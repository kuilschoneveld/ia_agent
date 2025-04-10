from enum import Enum


class ActionType(Enum):
    """
    There are four different types of actions. The value of the action types contains the function that should be
    executed, when an action of the respective task is executed. These functions make use of the data sources available
    to the agent, namely the ontology and twitter. Because the respective functionality is a property of the type of an
    action, this information is not stored in action.py.
    """
    NO_ACTION = (0, lambda data_sources, scenario: "")
    QUERY_ONTOLOGY = (1, lambda data_sources, scenario: data_sources["ontology"].execute_queries(scenario))
    QUERY_TWITTER = (2, lambda data_sources, scenario: data_sources["twitter"].execute_queries(scenario))
    RETURN_ANSWER = (3, lambda data_sources, scenario: "")
