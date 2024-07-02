"""This module contains the config dict schema to be used on general schemas for the application"""

from pydantic import ConfigDict

gen_config_dict = ConfigDict(
    use_enum_values=True,
    extra="ignore"
)