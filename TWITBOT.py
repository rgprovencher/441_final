# class object that uses API keys to interface with twitter. Used to check
# kickbot's twitter feed for kick commands, and to post the results of a
# twitter-commanded kick.

import tweepy

class Twitbot:
    
    def __init__(self):
        
        self.lastMention = ["tweet_id", "name", "user", "location"]
    
        # API keys stored in a seperate text file to keep them from being
        # visible to all developers.
        # note that code may fail to compile without the correct API keys
        with open("/home/pi/twitter-bots/keys", 'r') as f:
            keys = f.read().split("\n")
            
            # not "self.xxxx" bc these values aren't needed after init
            consumer = keys[0]
            consumer_secret = keys[1]
            access = keys[2]
            access_secret = keys[3]
            bearer = keys[4]


            # .OAuthHandler("API key", "API Key secret")
            auth = tweepy.OAuthHandler(consumer, consumer_secret)
            
            # auth.set_access_token("Access token", "Acess Token secret")
            auth.set_access_token(access, access_secret)
            
            # Creates a bot with authentications
            self.api = tweepy.API(auth)
  
    
    # posts string to twitter
    def post(self, string):
        self.api.update_status(string)
        
    
    # gets id of last post tweeted by bot
    def getLastTweetID(self):
        # get tweet id of last posted status
        tweet = self.api.user_timeline(screen_name='kickbot_UMD', count = 1)
        last_id = tweet[0].id
        return last_id
        

    # checks for new mentions, extracts location data
    def updateLastMention(self):

        try:
            # gets most recent mention
            mentions = self.api.mentions_timeline(count=1)

            for tweet in mentions:
                tweet_id = tweet.id
                
                # if no new @s have been posted since last update,
                # return false
                if (tweet_id == self.lastMention[0]):
                    return False
                
                # extracts location command from tweet text 
                text = self.api.get_status(tweet_id) # gets full text
                location = text.text.split('\n')     # splits text by newline
                # keeps only the location [1] and not "@kickbot_umd" [0]
                location = location[1]
                
                name = tweet.user.name
                user = tweet.user.screen_name
                self.lastMention = [tweet_id, name, user, location]
                
            return True
        
            
        except Exception as e:
            print("Last mention lookup error:\n")
            print(e)


            
        























