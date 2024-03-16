def throw(error: Exception | str) -> None:
    if isinstance(error, str):
        raise Exception(error)
    else:
        raise error
