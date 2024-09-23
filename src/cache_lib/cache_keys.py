from typing import Optional


def get_default_request_cache_key(
    url: str,
    method: str,
    params: Optional[dict],
):
    """
    Default key generation for requests. url is assumed to be without parameters
    """
    if params:
        sorted_params = '|'.join(sorted(f'{k}_{v}' for k, v in params.items()))
    else:
        sorted_params = '|'
    return f'{url}!{method}!{sorted_params}'
