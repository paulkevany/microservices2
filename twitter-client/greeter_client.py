 #Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging
import time
import random
import redis

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    totalTweets = 0
    while True:
        try:
            with grpc.insecure_channel('server:50051') as channel:
                stub = helloworld_pb2_grpc.GreeterStub(channel)
                print('Sending resonse!')
                for response in stub.SendTweetToClient(helloworld_pb2.TweetRequest(user='twitteruser')):
                    print('Response Sent!')
                    print(response, flush=True)
                    conn = redis.StrictRedis(host='redis', port=6379)
                    longestWord = calculateLongestWord(response.text)
                    print('Longest word in tweet: ' + longestWord)
                    conn.set("tweet.longestword" + response.text, longestWord)
                    conn.set("twitter.totalTweets", totalTweets)
                    totalTweets += 1
                    time.sleep(.5) 
        except Exception as ex: 
            print('Error: ', ex)


def calculateLongestWord(text):
    #Calculate the longest word in the tweet
    longest = 0
    word = ''
    for i in text.split(): 
        if len(i) > longest:
            word = i
            longest = len(i)
    return word
    
    


if __name__ == '__main__':
    logging.basicConfig()
    run()
