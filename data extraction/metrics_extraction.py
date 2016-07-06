import json 
import sys
import time

#Reading the file with json data into a list of dictionaries
def ReadJsonDictionary(file, list_l, topic):
	with open(file, 'r', encoding='utf-8') as f:
		for line in f:
			l = json.loads(line)
			list_l.append(l)
	return list_l


def Statistics(list_l, topic):
	#Defining useful variables
	users = set([])
	tweets = set([])
	user_friendship_coefficient = {}
	user_activity = {}
	verified_users = 0
	hashtags = {}
	hashtag_adj = []
	hashtag_adj_frequency = {}
	mentions = {}
	mention_adj = []
	mentions_adj_frequency = {}
	tuples_of_mentions = []
	tuples_of_hashtags = []
	places = {}
	audience = 0
	likes = 0
	likes_frequency = {}
	audience_frequency = {}
	
	#Sequentially process all the tweet objects in the list
	for item in list_l:
		tweets.add(item['id']) #Keep the set of tweet IDs
		#Checking the location attribute for the tweet
		if item['place']!= None: #If there's the location embeddedn in the tweet
			place = item['place']['country'] #Save the location country
			places = FrequencyCount(places, place) #Count the number of tweets from this country
			
		#Keep the set of user IDs	
		user = item['user']['id']
		users.add(user)
		
		#Compute the number of verified users
		if item['user']['verified'] == True:
			verified_users+=1
			
		#Compute the total adience
		audience_frequency[item['user']['id']] = item['user']['followers_count']
		audience = sum(audience_frequency.values())
		
		#Calculate the friendship coefficient of a user
		if item['user']['friends_count'] >0:
			user_friendship_coefficient[user] = float(item['user']['followers_count'])/float(item['user']['friends_count'])
		else:
			user_friendship_coefficient[user] = float(item['user']['followers_count'])
		user_activity[user] = item['user']['statuses_count']
		
		#Check if it is a retweet, to get the number of likes
		if 'retweeted_status' in item and 'favorite_count' in item['retweeted_status']:
			#Compute the distribution of likes per tweet
			likes_frequency[item['retweeted_status']['id']] = item['retweeted_status']['favorite_count']
		#Compute the total number of likes
		likes = sum(likes_frequency.values())

		#Extract entities data
		
		#Hashtags
		if len(item['entities']['hashtags'])>0: #If there are hashtags in the tweet
			hashtags_in_tweet = []
			for hashtag_num in range(0, len(item['entities']['hashtags'])):
				#Make a hashtag lowercase, to avoid dublicates and count correctly
				hashtag = item['entities']['hashtags'][hashtag_num]['text'].lower()
				hashtags_in_tweet.append(hashtag)
				#Count the overall frequency of a hashtag
				hashtags = FrequencyCount(hashtags, hashtag)
		#Create the adjacency list of hashtags for each tweet
		hashtag_adj.append(hashtags_in_tweet)
		
		#Mentions
		if len(item['entities']['user_mentions'])>0: #If there are mentions in the tweet
			mentions_in_tweet = []
			for mention_num in range(0,len(item['entities']['user_mentions'])):
				mention = item['entities']['user_mentions'][mention_num]['screen_name']
				mentions_in_tweet.append(mention)
				#Count the overall frequency of a mention
				mentions = FrequencyCount(mentions, mention)
		#Create the adjacency list of mentions for each tweet
		mention_adj.append(mentions_in_tweet)
	
	#Count the frequency of the pairs of hashtags that appear in the dataset
	for hashtag_adj_tweet in hashtag_adj:
		tuples_of_hashtags = AdjacencyList(hashtag_adj_tweet, tuples_of_hashtags)
	hashtag_adj_frequency = AdjacencyFrequencyCount(hashtag_adj_frequency, tuples_of_hashtags)
	
	
	#Count the frequency of the pairs of mentions that appear in the dataset
	for mention_adj_tweet in mention_adj:
		tuples_of_hashtags = AdjacencyList(mention_adj_tweet, tuples_of_mentions)
	mentions_adj_frequency = AdjacencyFrequencyCount(mentions_adj_frequency, tuples_of_mentions)

	#Print out useful stats
	print("For the topic "+topic+" basic statistics are the following:")
	print("There are "+ str(len(tweets)) + " tweets")
	print("From " + str(len(users)) + " users")
	print("Verified users "+ str(verified_users) + " (" + str(int(verified_users/len(users)*100))+"%)" )
	print("The total possible audience is " + str(audience) + " Twitter users")
	print("The total number of likes is " + str(likes))
	print("Number of unique hashtags: " + str(len(hashtags)))
	print("Number of unique mentions: " + str(len(mentions)))
	
	#Write metrics to the file for further analysis
	WriteDictionaryFile(user_activity, topic+"_user_activity", True)
	WriteDictionaryFile(user_friendship_coefficient, topic+"_user_friendship", True)
	WriteDictionaryFile(hashtags, topic+"_hashtags_frequency", True)
	WriteDictionaryFile(hashtag_adj_frequency, topic+"_hashtags_adjacency_frequency", True)
	WriteDictionaryFile(mentions, topic+"_mentions_frequency", True)
	WriteDictionaryFile(mentions_adj_frequency, topic+"_mentions_adjacency_frequency", True)
	WriteDictionaryFile(places, topic+"_locations_frequency", True)
	WriteDictionaryFile(likes_frequency, topic+"_likes_frequency", True)
	WriteDictionaryFile(audience_frequency, topic+"_audience_frequency", True)

#Count the frequency of tuples in the adjacency list
def AdjacencyFrequencyCount(dictionary, list_l):
	key = ""
	for item in list_l:
		x= sorted(item)
		key = str(x[0] + "-" + x[1])
		if key in dictionary:
			dictionary[key] = dictionary[key] +1
		else:
			dictionary[key] = 1

	return dictionary

#Create an adjacency list for each tuple of elements which appears together in the dataset
def AdjacencyList(items, list_h):
	if len(items) > 1:
		for item in items:
			for item2 in items:
				if item != item2:
					list_h.append([item, item2])
	return list_h

#Write a dictionary to a file
def WriteDictionaryFile(dictionary, file, sorted_b):
	with open(file, 'w', encoding = "utf-8") as f:
		if sorted_b: #If we need a sorted dictionary
			for key in sorted(dictionary, key=dictionary.get, reverse=True):
				f.write(str(key)+ ", "+ str(dictionary[key]) + '\n')
				f.flush()
		else: #If we don't need a sorted dictionary
			for key in dictionary:
				f.write(str(key)+ ", "+ str(dictionary[key]) + '\n')
				f.flush()

#Counting the number of times an element appears in the dataset
def FrequencyCount(freq_dictionary, item):
	if item in freq_dictionary:
		freq_dictionary[item] = freq_dictionary[item] + 1
	else:
		freq_dictionary[item] = 1
	return freq_dictionary


topic = str(sys.argv[1])
file_topic = str(sys.argv[2])

#List for dictionaries of tweet objects
data_topic = []

#Read the file with data
data_topic = ReadJsonDictionary(file_topic, data_topic, topic)

#Calculate the statistics
Statistics(data_topic, topic)
