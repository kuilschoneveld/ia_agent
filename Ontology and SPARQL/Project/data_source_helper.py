from abc import abstractmethod, ABC

from result import IResult


class IDataSourceHelper(ABC):
    """
    For every data source of the agent, a designated helper class exists. This class acts as an interface that is
    realized by all result data source helper classes, namely "OntologyHelper" and "TwitterHelper". It allows for
    easy addition of more data sources for the agent.
    """
    @abstractmethod
    def get_result_confidence(self) -> float:
        pass

    @abstractmethod
    def get_nl_explanation(self, positive) -> str:
        pass

    @abstractmethod
    def execute_queries(self, scenario) -> IResult:
        pass
