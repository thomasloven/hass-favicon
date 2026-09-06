import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

DOMAIN = "favicon"


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return await self.async_step_config()

    async def async_step_config(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Favicon", data=user_input)

        return self.async_show_form(
            step_id='config',
            data_schema=vol.Schema(
                {
                    vol.Optional('title'): str,
                    vol.Optional('icon_path'): str,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return EditFlow()


class EditFlow(config_entries.OptionsFlow):
    # Do not define __init__ and do not assign self.config_entry - since
    # HA 2025.12 OptionsFlow.config_entry is a read-only property that HA
    # populates for us.

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(
            step_id='init',
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        'title',
                        description={
                            "suggested_value": current.get("title", ""),
                        }
                    ): str,
                    vol.Optional(
                        'icon_path',
                        description={
                            "suggested_value": current.get("icon_path", ""),
                        }
                    ): str,
                }
            ),
        )
