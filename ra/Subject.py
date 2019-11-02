from abc import ABC, abstractmethod

class Subject(ABC):

    """
    The subject interface
    """
    observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    @abstractmethod
    def notify(self):
        # notify all observers about an event
        pass
