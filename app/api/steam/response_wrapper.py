from abc import abstractmethod


class ResponseWrapper:
    """
    To init a ResponseWrapper SubClass implement the constructor as init
    """

    def __init__(self, response) -> None:
        self.init(**response)

    @abstractmethod
    def init() -> None: return
