from abc import ABC, abstractmethod

class Observer(ABC):
    """
    The observer interface
    """

    @abstractmethod
    def update(self, subject):
        # receive update from subject
        pass