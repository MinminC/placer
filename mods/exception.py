from mods import *


class ConfigError(Exception):
    """
    app의 config가 비정상적일 때 발생하는 에러
    """
    def __init__(self):
        self.msg = ERROR_OPENDATA_CONFIG_ERROR_MSG

    def __str__(self):
        return self.msg
