from result import IResult


class OntologyQueryResult(IResult):
    """
    This class acts as a data class to store the query results from the ontology and make them available
    to the agent. It implements the interface IResult to allow action objects to check for an empty result.
    """

    def __init__(self):
        self.positive_results = {}
        self.negative_results = {}

    def get_total(self):
        query_results = [res for query in list(self.negative_results.values()) for res in query]
        total_instances = [instance for res in query_results for instance in res]
        return total_instances + self.get_positive()

    def get_positive(self):
        query_results = [res for query in list(self.positive_results.values()) for res in query]
        total_instances = [instance for res in query_results for instance in res]
        return total_instances

    def is_empty(self) -> bool:
        return not self.positive_results and not self.negative_results
