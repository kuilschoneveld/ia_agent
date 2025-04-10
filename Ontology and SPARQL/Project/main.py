import sys
import os

# Add the root directory to the system path to import load_env module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from load_env import load_environment
from agent import Agent


def main():
    # Load environment variables
    if not load_environment():
        print('\033[91m' + "Warning: Some environment variables are missing. Twitter functionality may be limited.")
        print('\033[0m')
    
    print('\033[91m' + "Hi, I am an intelligent, fake content detection agent. If you give me a statement or describe a scenario, I"
          " will tell you whether I think it is true or false.")
    print('\033[0m')

    scenarios = [  # supported scenarios
        "Healthy people are happy",
        "Individual sports require lower body",
        "Sugar is good for people"
    ]

    agent = Agent()

    user_scenario = input()

    while user_scenario != "Bye":
        result = agent.evaluate_scenario(user_scenario)
        print('\033[91m' + result)
        print('\033[0m')
        user_scenario = input()

    print('\033[91m' + "Good bye!")


if __name__ == "__main__":
    main()
