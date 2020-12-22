##########################
#       libraries        #
##########################

import json
import tweepy as tw
import time 
import datetime

#############################
#      authintication       #
#############################
path = r" "
### opening the tokens file ###
try:
    with open( path , "r") as json_tokens:
     tokens = json.loads(json_tokens.read())
except:
    print("file not found.")
### authinticating twitter api ###
try:
    auth =tw.OAuthHandler(tokens["API_KEY"], tokens["API_SECRET"])
    auth.set_access_token(tokens["ACCESS_TOKEN"], tokens["ACCESS_TOKEN_SECRET"])
    api = tw.API(auth)
except:
    print("invaild tokens/tokens not found")  

################################
#      helper functions        #
################################

### seperating the date from the time ###
# this was done to make it easier to store in the database  #
def get_date(date):
    for i in range(len(date)-1):
        if (date[i] == " "):
            date = date[:i]
            break
    return date   
    #---------------------------#
def get_time(date):
    for i in range(len(date)-1):
        if date[i] == " ":
            date = date[i+1:len(date)]
            break
    return date
# optinal: inserts the final set of tweets into json 
def intoJSN(file , content):
    with open(file , 'a+') as f:
        json.dump(content , f , indent= 4)

#######################################################################################
#                                                                                     #
#                     fetching and proccessing functions                              #
#                                                                                     #
#######################################################################################
# this function will extract the data from a tweets list #
# the paramater takes a list of tweets object            #
# you can chose whatever attributes you want by readin   #
# the doc of tweepy and checking the attributes of       #
# the tweet and user objects                             #
##########################################################
def process_tweets(tweet_list):
    t_list = []
    # iterating through the tweets list and extracting wanted attributes
    for tweet in tweet_list:
        t_list.append({
           "tweet_id": tweet.id_str, 
            "text": tweet.text.replace("\n" , "\\"),
            "likes": tweet.favorite_count,
            "in_reply_to": tweet.in_reply_to_screen_name,
            "retweet_count": tweet.retweet_count,
            "status_count" : str(tweet.user.statuses_count),
            "date_created_at":get_date(str(tweet.created_at)) ,
            "time_created_at":get_time(str(tweet.created_at)),
            "screen_name": tweet.user.screen_name,
            "retweeted": str(tweet.retweeted) 
            
            })
    #returning a list of dictionaries   
    return t_list   

####################################################################
# main tweets fetching function , takes a keywords parameter(words #
# that you will be searching for) , the maximum number of tweet s  #
# you want to fetch , and the batch which is how many you want to  #
# get each time , eg.: num_tweets = 300 and batch = 100 will fetch #
# 300 tweets in batchs of 100 each time                            #
# this will return an iterable list of tweet objects               #
####################################################################

def get_tweets(keywords ,  num_tweets , batch):
    tweets_list = []
    #starting with no spesific id
    maxID = None
    #main collecting loop
    while len(tweets_list) < num_tweets:
        #extending the tweets list with a tweet object , size  of it is that batch#
        tweets_list.extend(tw.Cursor(api.search , q = keywords , max_id = maxID , lang = 'en').items(batch))
        print("loaded {} / {} tweets".format(len(tweets_list) , num_tweets))
        #set the id to the tweet after the last tweet (to prevent duplicates)
        maxID = tweets_list[-1].id-1
        # tweepy limit is 900 per 15 minutes  , if you request more than 900 , the program halts until the limit rate is reset
        if(len(tweets_list) >= 900):
            time.sleep(900)
    return tweets_list   


############################
#     main function call   #
############################

def main():
    path = r" "
    tweets  = get_tweets("#COVID20", 100, 100)
    intoJSN(path, process_tweets(tweets))


if __name__ == "__main__":
    main()





