import logging

import homeassistant.components.frontend
from homeassistant.components.frontend import _frontend_root

_LOGGER = logging.getLogger(__name__)

DOMAIN = "favicon"

async def async_setup(hass, config):

    favicon = config[DOMAIN].get('favicon')
    apple = config[DOMAIN].get('apple')

    if favicon or apple:
        get_template = homeassistant.components.frontend.IndexView.get_template

        def new_get_template(self):
            tpl = get_template(self)
            render = tpl.render
            def new_render(*args, **kwargs):
                text = render(*args, **kwargs)
                if favicon:
                    text = text.replace("/static/icons/favicon.ico", favicon)
                if apple:
                    text = text.replace("/static/icons/favicon-apple-180x180.png", apple)
                return text
            tpl.render = new_render
            return tpl

        homeassistant.components.frontend.IndexView.get_template = new_get_template

    icons = []
    for size in config[DOMAIN]:
        if not isinstance(size, int):
            continue
        i = config[DOMAIN].get(size)
        if i:
            icons.append({
                "src": i,
                "sizes": f"{size}x{size}",
                "type": "image/png",
                })

    if icons:
        homeassistant.components.frontend.MANIFEST_JSON["icons"] = icons

    return True


