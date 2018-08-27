import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json


# To be initialized
consumer_key = 'iJn5rSoJkV3DmxkFKcV8fw32e'
consumer_secret = '8CLu0Lds11kiLTRSo4nGGQOzVL1rOp3GPUy7X6sacjXOQALrMc'
access_token = '3494481735-LpPHHPFCqnp27dNdSHnNmmqByaeUNOP3DE8wFq9'
access_secret = 'h7tkxHvisBX5VfVKyT0rm79kmVNTH2wkOUL5xG9YaLsdy'

# topics we want to track
TOPICS = ['dog']
PORT = 7777

class TweetsListener(StreamListener):

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def on_data(self, data):
        try:
            msg = json.loads(data)
            print(msg['text'])            
            text = msg['text'].encode('utf-8')
            self.client_socket.send(text)
            return True
        except BaseException as e:
            print("Error on_data: {}".format(str(e)))
        return True

    def on_error(self, status):
        print(status)
        return True


def sendData(client_socket):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # launch twitter stream and filter by selected topics
    twitter_stream = Stream(auth, TweetsListener(client_socket))
    twitter_stream.filter(track=TOPICS)

if __name__ == "__main__":
    socket = socket.socket()
    host = "127.0.0.1"          # localhost
    socket.bind((host, PORT))

    print("Listening on port: {}".format(str(PORT)))

    socket.listen(5)                 # wait for client connection
    client_socket, addr = socket.accept()        # Establish connection with client
    print("Received request from:", str(addr))
    sendData(client_socket)