
# coding: utf-8

# In[1]:


import os
import pandas as pd
import tweepy
import time
import spacy
import en_core_web_sm
import matplotlib

matplotlib.use("Agg")
from config import consumer_key, consumer_secret, access_token, access_token_secret

# Get config variable from environment variables
#consumer_key = os.environ.get("consumer_key")
#consumer_secret = os.environ.get("consumer_secret")
#access_token = os.environ.get("access_token")
#access_token_secret = os.environ.get("access_token_secret")

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Load model
nlp = en_core_web_sm.load()


# In[2]:


def update_twitter():

    # Create dictionary to hold text and label entities
    tweet_dict = {"text": [], "label": []}

    mentions = api.search(q="@realDonaldTrump Congratulations")
    print(mentions["statuses"][0]["text"])
    words = []
    try:
        command = mentions["statuses"][0]["text"]
        words = command.split("Congratulations")
        target_account = words[1].strip()
        print(target_account)
        user_tweets = api.user_timeline(target_account, page=1)

        # Loop through tweets
        for tweet in user_tweets:
            #print(tweet["user"]["name"])
            # Use nlp on each tweet
            doc = nlp(tweet["text"])
            
            # Check if nlp returns no entities
            if not doc.ents:
                print("No entities to visualize")
                print("----------------------------")
            else:
                # Print the entities for each doc
                for ent in doc.ents:
                    # Store entities in dictionary
                    tweet_dict["text"].append(ent.text)
                    tweet_dict["label"].append(ent.label_)
        # Convert dictionary to DataFrame
        tweet_df = pd.DataFrame(tweet_dict)
        tweet_df.head()

        # Group by labels# Group
        label_frequency = tweet_df.groupby(["label"]).count()

        # Get bar graph as a figure and tweet chart
        bar = label_frequency.plot.bar()
        fig = bar.get_figure()
        fig.savefig("box.png")
        api.update_with_media(
            "box.png", "Break down of tweet labels for " + target_account
        )
    except Exception:
        raise

    


# In[3]:


days = 0
while days < 2:
    print("Updating Twitter")

    # Update the twitter
    update_twitter()

    # Wait a day
    time.sleep(3)

    # Update day counter
    days += 1


# In[ ]:




