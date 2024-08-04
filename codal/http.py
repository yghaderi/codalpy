from typing import Literal, Any
import requests
from pydantic import BaseModel
from requests.exceptions import HTTPError, Timeout, RequestException, ConnectionError

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}


def get(
    url,
    params: dict[str, Any],
    rtype: Literal["josn", "text"],
    timeout: tuple[int, int] = (2, 10),
):

    try:
        r = requests.get(url=url, params=params, timeout=timeout, headers=HEADERS)
        match rtype:
            case "josn":
                return r.json()
            case "text":
                return r.text
    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Timeout as e:
        print(f"Timeout error occurred: {e}")
    except RequestException as e:
        print(f"n error error occurred: {e}")
