from action_type import ActionType


class Action:
    """
    An action represents a state transition in the environment. Every action is of certain action type.
    """
    def __init__(self, action_type):
        self.no_result = None
        if action_type == ActionType.NO_ACTION:
            self.no_result = False
        self.action_type = action_type

    def execute(self, data_sources, scenario):
        """
        Execute functionality, which is assigned to the action type.
        :param scenario: scenario to be evaluated
        :param data_sources: all data sources available to the agent including query results
        :return: data sources with possibly updated query results
        """
        result = self.action_type.value[1](data_sources, scenario)
        if result != "":
            self.no_result = result.is_empty()

        return data_sources
