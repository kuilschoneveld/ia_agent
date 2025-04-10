from abc import ABC, abstractmethod


class IResult(ABC):
    """
    For every data source of the agent, a designated result class exists. As an instance of the class "Action" is not
    aware of the type of result it deals with, this class acts as an interface that is realized by all result classes,
    namely "OntologyQueryResult" and "TwitterQueryResult".
    """
    @abstractmethod
    def is_empty(self) -> bool:
        pass
