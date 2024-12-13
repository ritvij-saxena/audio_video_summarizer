from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    """
    Abstract base class for all processors.
    Ensures that each processor implements the necessary methods.
    """
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def process(self):
        """
        Processes the input arguments and performs the desired operation.
        """
        pass

    def print_summary(self, summary):
        print(f"\nSummary: \n {summary}")
