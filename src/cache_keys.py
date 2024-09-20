def get_default_request_cache_key(
    url: str,
    method: str,
    params: dict,
):
    """
    Default key generation for requests. url is assumed to be without parameters
    """
    sorted_params = '|'.join(sorted(f'{k}_{v}' for k, v in params.items()))
    return f'{url}!{method}!{sorted_params}'
