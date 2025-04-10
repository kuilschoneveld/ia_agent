import re
import tweepy
import os
from tweepy import OAuthHandler
from textblob import TextBlob
from twitter_query_result import TwitterQueryResult
from data_source_helper import IDataSourceHelper
# import nltk
# from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from result import IResult


class TwitterHelper(IDataSourceHelper):

    def __init__(self):
        """
        Twitter API authentication using environment variables.
        Create a .env file with your API credentials.
        See .env.example for required variables.
        """
        # Load API keys from environment variables
        consumer_key = os.environ.get('TWITTER_CONSUMER_KEY', '')
        consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET', '')
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN', '')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', '')
        bearer_token = os.environ.get('TWITTER_BEARER_TOKEN', '')

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            # # self.api = tweepy.Client(bearer_token=bearer_token)

        except tweepy.TweepError as e:
            # print("Error: Authentication Failed")
            print("Error : " + str(e))

        self.stemmer = PorterStemmer()
        self.result = TwitterQueryResult()

    def get_result_confidence(self) -> float:
        """
        The method "get_result_confidence" returns an interpretation of the query result from twitter. A negative
        number indicates that the given scenario is found to contain fake information. A positive number indicates that
        the given scenario is truthful. The number also indicates the confidence of twitter. The closer the number
        is to 0, the less confident twitter is about the given scenario.
        :return: interpretation of query result
        """
        # calling function to get tweets
        # tweets = self.execute_queries(query='', count=2000)
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in self.result.tweets if tweet['sentiment'] == 'positive']
        # # percentage of positive tweets
        # print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(self.result)))
        # # picking negative tweets from tweets
        ntweets = [tweet for tweet in self.result.tweets if tweet['sentiment'] == 'negative']
        # # percentage of negative tweets
        # print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(self.result)))
        # # percentage of neutral tweets
        # print("Neutral tweets percentage: {} % \
        #     ".format(100 * (len(self.result) - (len(ntweets) + len(ptweets))) / len(self.result)))

        # # printing first 5 positive tweets
        # print("\n\nPositive tweets:")
        # for tweet in ptweets[:10]:
        #     print(tweet['text'])
        #
        # # printing first 5 negative tweets
        # print("\n\nNegative tweets:")
        # for tweet in ntweets[:10]:
        #     print(tweet['text'])

        number_of_results = len(self.result.tweets)
        # number_of_positive_results = len(self.result.positive_results)
        if number_of_results >= 0 and len(ptweets) > 0:
            return (1 / (number_of_results / len(ptweets)) - 0.5) * 2

        return 0

    def get_nl_explanation(self, positive) -> str:
        confidence = self.get_result_confidence()

        answer = "My search on twitter "
        if confidence == 0:
            answer += "has not yielded any result for this statement."
            return answer

        if (positive and confidence > 0) or (not positive and confidence < 0):
            answer += "confirmed this result."
        if (positive and confidence < 0) or (not positive and confidence > 0):
            answer += "contradicted this result but did not provide a lot of evidence for it."

        return answer

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def execute_queries(self, query, count=10) -> IResult:
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_tweets(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            # print(tweets)
            # return parsed tweets
            # return tweets
            self.result.tweets = tweets

        except tweepy.errors.TweepyException as e:
            # print error (if any)
            print("Error : " + str(e))

        return self.result

    def form_query(self, query):
        query = query.lower()
        tokens = word_tokenize(query)
        for i in range(len(tokens)):
            tokens[i] = self.stemmer.stem(tokens[i])
        return ' '.join(tokens)


