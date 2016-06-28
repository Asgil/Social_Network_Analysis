import tweepy
import json
import sys
import time

query = str(sys.argv[1])
consumer_token = ''
consumer_secret = ''
key = ''
secret = ''

#Authentication
#More on http://docs.tweepy.org/en/v3.5.0/auth_tutorial.html
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)


#Creting stream listener
#More on http://docs.tweepy.org/en/v3.5.0/streaming_how_to.html?highlight=stream
class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		with open(query+".json", "a", encoding='utf-8') as f:
			#Writing down to json file the statuses we get from twitter
			dictionary = status._json
			json.dump(dictionary, f)
			f.write("\n")



	def on_error(self, status_code):
		print(status_code)
		if status_code == 420:
			#Handling rate limit restrictions
			print("sleeping")
			time.sleep(60*15)


#Launching the stream listener
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

try:
	myStream.filter(track=[query])
except TypeError as e:
	print(e)