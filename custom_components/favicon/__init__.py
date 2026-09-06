import html
import json
import logging
import os
import re

import voluptuous as vol

import homeassistant.components.frontend as frontend
import homeassistant.helpers.config_validation as cv


_LOGGER = logging.getLogger(__name__)

DOMAIN = "favicon"

RE_APPLE = r"^favicon-apple-"
RE_ICON = r"^favicon-(\d+x\d+)\..+"

CONFIG_TITLE = "title"
CONFIG_ICON_PATH = "icon_path"

DATA_GET_TEMPLATE = "get_template"
DATA_MANIFEST_ICONS = "manifest_icons"

# The strings we substitute in the rendered index.html. If the frontend ever
# renames these the integration silently stops having an effect, so warn.
MARKER_FAVICON = "/static/icons/favicon.ico"
MARKER_APPLE = "/static/icons/favicon-apple-180x180.png"
MARKER_TITLE = "<title>Home Assistant</title>"
MARKER_BODY = "<body>"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONFIG_TITLE): cv.string,
                vol.Optional(CONFIG_ICON_PATH): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    data = hass.data.setdefault(DOMAIN, {})

    # Stash the pristine versions of everything we are about to patch, so
    # that removing the integration can put them back.
    if DATA_GET_TEMPLATE not in data:
        data[DATA_GET_TEMPLATE] = frontend.IndexView.get_template
    if DATA_MANIFEST_ICONS not in data:
        data[DATA_MANIFEST_ICONS] = frontend.MANIFEST_JSON["icons"].copy()

    conf = config.get(DOMAIN)
    if not conf:
        return True
    _store_conf(hass, conf)
    return await apply_hooks(hass)


async def async_setup_entry(hass, config_entry):
    config_entry.async_on_unload(
        config_entry.add_update_listener(_update_listener)
    )
    return await _update_listener(hass, config_entry)


async def async_unload_entry(hass, config_entry):
    return remove_hooks(hass)


async def async_remove_entry(hass, config_entry):
    return remove_hooks(hass)


def _store_conf(hass, conf):
    """Replace the current title/icon_path settings with ``conf``."""
    data = hass.data[DOMAIN]
    for key in (CONFIG_ICON_PATH, CONFIG_TITLE):
        data.pop(key, None)
    data.update(conf)


async def _update_listener(hass, config_entry):
    # A config entry's options are empty until the user opens the options
    # flow for the first time, so fall back to the data supplied on creation.
    # Note: config entry attributes are read-only since HA 2024.11, so we
    # must not try to assign entry.options here.
    conf = {**config_entry.data, **config_entry.options}
    _store_conf(hass, conf)
    return await apply_hooks(hass)


def _url_join(path, filename):
    """Join a frontend path and a filename with a forward slash.

    os.path.join() would produce a backslash on Windows and break the URL.
    """
    return path.rstrip("/") + "/" + filename


def find_icons(hass, path):

    icons = {}
    manifest = []
    if not path:
        return icons
    if not path.startswith("/local/"):
        _LOGGER.error(
            "icon_path must be a frontend path starting with /local/, got: %s",
            path,
        )
        return icons

    localpath = hass.config.path("www" + path[len("/local"):])
    _LOGGER.debug("Looking for icons in: %s", localpath)
    try:
        filenames = os.listdir(localpath)
    except OSError as err:
        _LOGGER.error("Could not read icon directory %s: %s", localpath, err)
        return icons

    for fn in filenames:
        if fn == "favicon.ico":
            icons["favicon"] = _url_join(path, fn)
        if re.search(RE_APPLE, fn):
            icons["apple"] = _url_join(path, fn)
        if icon := re.search(RE_ICON, fn):
            manifest.append({
                "src": _url_join(path, fn),
                "sizes": icon.group(1),
                "type": "image/png",
                })

    if manifest:
        icons["manifest"] = manifest

    if not icons:
        _LOGGER.warning(
            "No icons found in %s - filenames must be favicon.ico, "
            "favicon-apple-<anything>.png or favicon-<size>x<size>.png",
            localpath,
        )
    else:
        _LOGGER.debug("Found icons: %s", icons)
    return icons


def _title_script(title):
    """Build the script that keeps the tab and sidebar titles overridden.

    ``title`` is embedded via json.dumps so quotes and backslashes in a user
    supplied title cannot break out of the JS string literal, and any "</" is
    escaped so it cannot terminate the <script> element early.
    """
    js_title = json.dumps(title).replace("</", "<\\/")
    return TITLE_SCRIPT_TEMPLATE.replace("%%TITLE%%", js_title)


TITLE_SCRIPT_TEMPLATE = """
    <script type="module">
      (() => {
        const TITLE = %%TITLE%%;

        // Tab title: Home Assistant rewrites document.title on navigation,
        // so watch the <title> element instead of polling on a timer.
        const titleEl = document.querySelector("title");
        if (titleEl) {
          let lastSet = null;
          const fixTitle = () => {
            const current = document.title;
            // Guard against re-triggering ourselves, which would otherwise
            // loop forever if TITLE itself contains "Home Assistant".
            if (current === lastSet) return;
            const fixed = current.replace(/Home Assistant/g, TITLE);
            if (fixed === current) return;
            lastSet = fixed;
            document.title = fixed;
          };
          new MutationObserver(fixTitle).observe(titleEl, {
            childList: true,
            characterData: true,
            subtree: true,
          });
          fixTitle();
        }

        // Sidebar title. ha-sidebar renders it from a reactive property, so
        // re-apply after every render rather than only once.
        customElements.whenDefined("ha-sidebar").then(() => {
          const Sidebar = customElements.get("ha-sidebar");
          if (!Sidebar || Sidebar.__faviconPatched) return;
          Sidebar.__faviconPatched = true;
          const updated = Sidebar.prototype.updated;
          Sidebar.prototype.updated = function (changedProperties) {
            if (updated) updated.call(this, changedProperties);
            const el = this.shadowRoot &&
                       this.shadowRoot.querySelector(".title");
            if (el && el.textContent !== TITLE) el.textContent = TITLE;
          };
        });
      })();
    </script>
    """


def _clear_template_cache(hass):
    """Drop the cached index template so it is re-rendered with our hooks."""
    for resource in hass.http.app.router.resources():
        if isinstance(resource, frontend.IndexView):
            resource._template_cache = None
    # HA >= 2024.7 also caches the *rendered* index in an lru_cache
    render_cache = getattr(frontend, "_async_render_index_cached", None)
    if render_cache is not None and hasattr(render_cache, "cache_clear"):
        render_cache.cache_clear()


async def apply_hooks(hass):
    data = hass.data.get(DOMAIN, {})
    icons = await hass.async_add_executor_job(
        find_icons,
        hass,
        data.get(CONFIG_ICON_PATH)
        )
    title = data.get(CONFIG_TITLE)

    def _get_template(self):
        tpl = data[DATA_GET_TEMPLATE](self)
        render = tpl.render

        def new_render(*args, **kwargs):
            text = render(*args, **kwargs)
            missing = []

            def substitute(marker, replacement):
                nonlocal text
                if marker not in text:
                    missing.append(marker)
                    return
                text = text.replace(marker, replacement)

            if "favicon" in icons:
                substitute(MARKER_FAVICON, icons["favicon"])
            if "apple" in icons:
                substitute(MARKER_APPLE, icons["apple"])
            if title:
                substitute(
                    MARKER_TITLE, f"<title>{html.escape(title)}</title>"
                )
                substitute(MARKER_BODY, MARKER_BODY + _title_script(title))

            if missing:
                _LOGGER.warning(
                    "Could not find %s in the frontend index page - this "
                    "version of Home Assistant is probably not supported by "
                    "the favicon integration any more",
                    ", ".join(missing),
                )

            return text

        tpl.render = new_render
        return tpl

    frontend.IndexView.get_template = _get_template
    _clear_template_cache(hass)

    if "manifest" in icons:
        frontend.add_manifest_json_key("icons", icons["manifest"])
    else:
        frontend.add_manifest_json_key(
            "icons", data[DATA_MANIFEST_ICONS].copy()
        )

    if title:
        frontend.add_manifest_json_key("name", title)
        frontend.add_manifest_json_key("short_name", title)
    else:
        frontend.add_manifest_json_key("name", "Home Assistant")
        frontend.add_manifest_json_key("short_name", "Home Assistant")

    return True


def remove_hooks(hass):
    data = hass.data[DOMAIN]
    frontend.IndexView.get_template = data[DATA_GET_TEMPLATE]
    _clear_template_cache(hass)
    frontend.add_manifest_json_key("icons", data[DATA_MANIFEST_ICONS].copy())
    frontend.add_manifest_json_key("name", "Home Assistant")
    frontend.add_manifest_json_key("short_name", "Home Assistant")
    return True
