import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

@config_entries.HANDLERS.register("favicon")
class ExampleConfigFlow(config_entries.ConfigFlow):
    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return await self.async_step_config()

    async def async_step_config(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                    title="", data=user_input)

        return self.async_show_form(
            step_id='config',
            data_schema=vol.Schema(
                {
                    vol.Optional('title'): str,
                    vol.Optional('favicon'): str,
                    vol.Optional('icon-apple'): str,
                    vol.Optional('icon-1024'): str,
                    vol.Optional('icon-512'): str,
                    vol.Optional('icon-384'): str,
                    vol.Optional('icon-192'): str,

                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ExampleEditFlow(config_entry)

class ExampleEditFlow(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id='init',
            data_schema=vol.Schema(
                {
                    vol.Optional('title',
                        default=self.config_entry.options.get("title", "")): str,
                    vol.Optional('favicon',
                        default=self.config_entry.options.get("favicon", "")): str,
                    vol.Optional('icon-apple',
                        default=self.config_entry.options.get("icon-apple", "")): str,
                    vol.Optional('icon-1024',
                        default=self.config_entry.options.get("icon-1024", "")): str,
                    vol.Optional('icon-512',
                        default=self.config_entry.options.get("icon-512", "")): str,
                    vol.Optional('icon-384',
                        default=self.config_entry.options.get("icon-384", "")): str,
                    vol.Optional('icon-192',
                        default=self.config_entry.options.get("icon-192", "")): str,

                }
            ),
        )

