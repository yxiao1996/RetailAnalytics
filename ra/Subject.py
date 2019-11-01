from abc import ABC, abstractmethod

class Subject(ABC):

    """
    The subject interface
    """

    @abstractmethod
    def attach(self, observer):
        # attach a observer to the subject
        pass

    @abstractmethod
    def detach(self, observer):
        # detach an observer from the subject
        pass

    @abstractmethod
    def notify(self):
        # notify all observers about an event
        pass
