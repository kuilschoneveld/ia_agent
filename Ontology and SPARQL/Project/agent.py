import logging

from environment_state import EnvironmentState
from internal_state import InternalState
from action import Action
from action_type import ActionType
from ontology_helper import OntologyHelper
from twitter_helper import TwitterHelper

logging.getLogger().setLevel(logging.WARN)


class Agent:

    def __init__(self):
        self.environment_state = EnvironmentState("", 0)
        self.previous_veracity = 0

        self.internal_state = InternalState(-1, -1)
        self.recent_action = Action(ActionType.NO_ACTION)

        self.starting_state = True

        self.data_sources = {
            "ontology": OntologyHelper(),
            "twitter": TwitterHelper()
        }
        self.ontology_trust = 0.5
        self.twitter_trust = 0.5

    def reset(self):
        self.__init__()

    def evaluate_scenario(self, scenario):
        """
        The function "evaluate_scenario" calls the agent function ("agent_function") and updates the environment state
        until all obtainable information is collected, more specifically until the recent action is of type
        ActionType.NO_ACTION or ActionType.RETURN_ANSWER.
        :param scenario: user input to be evaluated
        :return: explanation in natural language as to how the agent evaluates the given scenario
        """
        self.environment_state = EnvironmentState(scenario, 0)

        while self.recent_action.action_type != ActionType.RETURN_ANSWER or self.starting_state:
            self.log()

            next_action = self.agent_function()
            self.data_sources = next_action.execute(self.data_sources, self.environment_state.scenario)
            self.recent_action = next_action
            self.update_environment_state()

            self.starting_state = False

        last_env_state = self.environment_state
        ontology_explanation = self.data_sources["ontology"].get_nl_explanation(last_env_state.veracity > 0)
        twitter_explanation = self.data_sources["twitter"].get_nl_explanation(last_env_state.veracity > 0)

        self.log()
        self.reset()

        return self.construct_answer(last_env_state, ontology_explanation, twitter_explanation)

    def agent_function(self):
        """
        The function "agent_function" updates the internal state and obtains the next action from function
        "rule_matching"
        :return: action = next action to take
        """
        self.update_internal_state()
        return self.rule_matching()

    def rule_matching(self):
        """
        The function "rule_matching" takes as input the current internal state and returns an action. It implements
        the condition-action rules.
        :return: action = next action to take
        """
        if self.internal_state.ontology_queried == -1:  # refers to internal state (-1, -1)
            return Action(ActionType.QUERY_ONTOLOGY)
        if self.internal_state.twitter_queried == -1:  # refers to internal states (0, -1) and (1, -1)
            return Action(ActionType.QUERY_TWITTER)
        return Action(ActionType.RETURN_ANSWER)  # refers to internal states (0, 0), (0, 1), (1, 0), (1, 1)

    def update_environment_state(self):
        """
        The function "update_environment_state" implements the environment state transitions. Every action taken
        changes the veracity of the environment state.
        """
        self.previous_veracity = self.environment_state.veracity
        recent_action_type = self.recent_action.action_type

        if recent_action_type == ActionType.NO_ACTION or recent_action_type == ActionType.RETURN_ANSWER:
            return

        if recent_action_type == ActionType.QUERY_ONTOLOGY and not self.recent_action.no_result:
            self.environment_state.veracity = \
                self.previous_veracity + self.ontology_trust * self.data_sources["ontology"].get_result_confidence()
        elif recent_action_type == ActionType.QUERY_TWITTER and not self.recent_action.no_result:
            self.environment_state.veracity = \
                self.previous_veracity + self.twitter_trust * self.data_sources["twitter"].get_result_confidence()

    def update_internal_state(self):
        """
        The function "update_internal_state" represents the model of the agent, meaning the knowledge of the agent of
        how the world works. It updates the internal state depending on the previous veracity, current veracity
        and current internal state. If the veracity has not changed, the internal state will stay the same.
        """
        current_internal_state = self.internal_state
        current_veracity = self.environment_state.veracity

        if self.starting_state:
            return

        if self.recent_action.action_type == ActionType.QUERY_ONTOLOGY and current_veracity != self.previous_veracity:
            self.internal_state = InternalState(1, current_internal_state.twitter_queried)
        elif self.recent_action.action_type == ActionType.QUERY_ONTOLOGY and current_veracity == self.previous_veracity:
            self.internal_state = InternalState(0, current_internal_state.twitter_queried)
        elif self.recent_action.action_type == ActionType.QUERY_TWITTER and current_veracity != self.previous_veracity:
            self.internal_state = InternalState(current_internal_state.ontology_queried, 1)
        elif self.recent_action.action_type == ActionType.QUERY_TWITTER and current_veracity == self.previous_veracity:
            self.internal_state = InternalState(current_internal_state.ontology_queried, 0)

    def construct_answer(self, last_env_state, ontology_explanation, twitter_explanation):
        veracity = last_env_state.veracity
        scenario = last_env_state.scenario

        if veracity == 0:
            return "I could not come to a conclusion whether the statement \"" + scenario + "\" is true, because " \
                    "there is contradicting evidence."

        answer = ""
        if veracity > 0.5:
            answer += "I concluded with high confidence that the statement \"" + scenario + "\" is true."
        elif veracity > 0:
            answer += "I concluded that the statement \"" + scenario + "\" is true."
        elif veracity < -0.5:
            answer += "I concluded with high confidence that the statement \"" + scenario + "\" is false."
        elif veracity < 0:
            answer += "I concluded that the statement \"" + scenario + "\" is false."

        answer += " I arrived at this conclusion by using my own knowledge about the world as well as twitter as an" \
                  " external source of knowledge."
        answer += "\n" + ontology_explanation + "\n" + twitter_explanation

        return answer

    def log(self):
        logging_message = " Veracity: " + str(self.environment_state.veracity) + " "\
                          "Recent action: " + str(self.recent_action.action_type.value[0])
        logging.info(logging_message)
