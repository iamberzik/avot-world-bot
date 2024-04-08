import os
from typing import Callable

from api.conf import refresh_tokens
from core.globals import *
from core.utils import get_debug_mode


def request(url: str, debug: bool = get_debug_mode()):
    def decorator(func: Callable):

        def wrapper(*args, **kwargs):

            request_url = os.getenv(ENV_API_URL_KEY) + url

            try:
                response = func(*args, **kwargs, url=request_url)
                response.raise_for_status()

                result = response.json()

                if debug:
                    print(result)

                return result
            except Exception as e:

                refresh_tokens()
                response = func(*args, **kwargs, url=request_url)
                response.raise_for_status()

                result = response.json()

                if debug:
                    print(result)

                return result

        return wrapper

    return decorator
