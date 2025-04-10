from result import IResult


class TwitterQueryResult(IResult):

    def __init__(self):
        self.tweets = []

    def is_empty(self) -> bool:
        return self.tweets == []
