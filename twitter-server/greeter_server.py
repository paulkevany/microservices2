# Copyright 2015 gRPC authors.
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
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import redis
import datetime
import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import pandas as pd


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SendTweetToClient(self, request_iterator, context): 
         #read csv file 
        columns = ["target", "id", "date", "flag", "user", "text"]
        tweets = pd.read_csv('tweets.csv', names=columns, error_bad_lines=False, encoding="ISO-8859-1")
        #error_bad_line=False in the above makes it so that the application won't fail if it finds a comma in the text. 

        for index, row in tweets.iterrows():
            response = helloworld_pb2.TweetReply(target=row['target'], id=row['id'], date=row['date'], flag=row['flag'], user=row['user'], text=row['text'])
            try:
                conn = redis.StrictRedis(host='redis', port=6379)
                conn.set("log.server.tweet" + row['date'], row['text'])
            except Exception as ex: 
                print('Error: ', ex)
            yield response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('server:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
