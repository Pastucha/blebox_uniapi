from .feature import Feature
from .error import BadOnValueError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .box import Box

TV_LIFT_CONTROL_TYPES_API = {
    0: {
        "1": "open_or_stop",
        "2": "close_or_stop"
    },
    1: {
        "1": "up_or_stop",
        "2": "down_or_stop"
    },
    2: {
        "1": "up_or_stop",
        "2": "down_or_stop"
    },
    3: {
        "1": "up_or_stop",
        "2": "down_or_stop"
    },
    4: {
        "1": "open_or_stop",
        "2": "close_or_stop",
        "3": "to_fav"
    },
}


class Button(Feature):
    def __init__(self, product: "Box", alias: str, methods: dict, query_string: str) -> None:
        super().__init__(product, alias, methods)
        self._device_class = "UPDATE"
        self.query_string: str = query_string

    @classmethod
    def many_from_config(cls, product, box_type_config, extended_state):
        object_list = list()
        if len(box_type_config) > 0:
            alias = box_type_config[0]
            if isinstance(extended_state, dict) and extended_state is not None:
                lift_mode = extended_state.get('tvLift', {}).get('controlType', None)
                for row in TV_LIFT_CONTROL_TYPES_API[lift_mode].items():
                    indicator, endpoint = row
                    object_list.append(cls(product, alias + "_" + endpoint, {}, endpoint))

                return object_list
        else:
            return []

    async def set(self):
        await self.async_api_command("set", self.query_string)

    def after_update(self) -> None:
        pass


    def get_icon(self):
        '''Return icon for endpoint.'''
        if 'up' in self.query_string:
            return "mdi:arrow-up-circle"
        elif 'down' in self.query_string:
            return "mdi:arrow-down-circle"
        elif 'fav' in self.query_string:
            return "mdi:heart-circle"
        elif 'open' in self.query_string:
            return "mdi:arrow-up-circle"
        elif 'close' in self.query_string:
            return "mdi:arrow-down-circle"
        else:
            return ""
