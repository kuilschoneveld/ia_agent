class InternalState:
    """
    The instance variables of "InternalState" are not booleans but Integers of set [-1, 0, 1].
    """
    def __init__(self, ontology_queried, twitter_queried):
        self.ontology_queried = ontology_queried
        self.twitter_queried = twitter_queried
