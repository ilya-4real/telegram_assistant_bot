from abc import ABC, abstractmethod

class AbstractApiPoller(ABC):
    """api poller interface"""
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def poll_data():
        raise NotImplementedError