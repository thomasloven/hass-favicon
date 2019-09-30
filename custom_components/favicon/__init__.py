import logging
from collections import defaultdict

import homeassistant.components.frontend
from homeassistant.components.frontend import _frontend_root

_LOGGER = logging.getLogger(__name__)

DOMAIN = "favicon"

async def async_setup(hass, config):
    if not hass.data.get(DOMAIN):
        hass.data[DOMAIN] = defaultdict(int)

    if not hass.data[DOMAIN].get("get_template"):
        hass.data[DOMAIN]["get_template"] = homeassistant.components.frontend.IndexView.get_template

    conf = config.get(DOMAIN)
    if not conf:
        return True
    hass.data[DOMAIN].update(conf)
    return apply_hooks(hass)

async def async_setup_entry(hass, config_entry):
    config_entry.add_update_listener(_update_listener)
    config_entry.options = config_entry.data
    return await _update_listener(hass, config_entry)

async def async_remove_entry(hass, config_entry):
    return remove_hooks(hass)

async def _update_listener(hass, config_entry):
    conf = config_entry.options
    hass.data[DOMAIN].update(conf)
    return apply_hooks(hass)


def apply_hooks(hass):
    data = hass.data[DOMAIN]
    def _get_template(self):
        tpl = data["get_template"](self)
        render = tpl.render

        def new_render(*args, **kwargs):
            text = render(*args, **kwargs)
            if data["favicon"]:
                text = text.replace("/static/icons/favicon.ico", data["favicon"])
            if data["icon-apple"]:
                text = text.replace("/static/icons/favicon-apple-180x180.png", data["icon-apple"])
            if data["title"]:
                text = text.replace("<title>Home Assistant</title>", f"<title>{data['title']}</title>")
            return text

        tpl.render = new_render
        return tpl

    custom_manifest = dict(homeassistant.components.frontend.MANIFEST_JSON)

    if data["title"]:
        custom_manifest["name"] = data["title"];
        custom_manifest["short_name"] = data["title"]

    if data["icon-1024"] or data["icon-512"] or data["icon-384"] or data["icon-192"]:
        custom_icons = []

        if data["icon-1024"]:
            custom_icons.append({ "sizes": "1024x1024", "src": data["icon-1024"], "type": "image/png" })
        if data["icon-512"]:
            custom_icons.append({ "sizes": "512x512", "src": data["icon-512"], "type": "image/png" })
        if data["icon-384"]:
             custom_icons.append({ "sizes": "384x384", "src": data["icon-384"], "type": "image/png" })
        if data["icon-192"]:
             custom_icons.append({ "sizes": "192x192", "src": data["icon-192"], "type": "image/png" })

        custom_manifest["icons"] = custom_icons

    homeassistant.components.frontend.MANIFEST_JSON = custom_manifest
    homeassistant.components.frontend.IndexView.get_template = _get_template
    return True

def remove_hooks(hass):
    data = hass.data[DOMAIN]
    homeassistant.components.frontend.IndexView.get_template = data["get_template"]
    return True

