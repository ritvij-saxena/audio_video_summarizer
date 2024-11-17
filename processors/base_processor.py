from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    """
    Abstract base class for all processors.
    Ensures that each processor implements the necessary methods.
    """

    @abstractmethod
    def process(self):
        """
        Processes the input arguments and performs the desired operation.
        """
        pass
