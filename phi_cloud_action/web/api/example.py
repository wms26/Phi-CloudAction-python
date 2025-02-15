from abc import ABC, abstractmethod

class example(ABC):
    def __init__(self):
        self.route_path = "/example"
        self.methods = ["GET"]

    @abstractmethod
    def __call__(self):
        pass
