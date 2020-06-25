import os
import time
import re
import slackclient
import pandas as pd
import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.stem import wordnet
nltk.download('stopwords')
from nltk import pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
stopwords = stopwords.words('english')
import nltk
from nltk import word_tokenize, sent_tokenize
from sklearn.metrics import pairwise_distances # to perfrom cosine similarity
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer # to perform bow
from sklearn.feature_extraction.text import TfidfVectorizer # to perform tfidf


# instantiate Slack client
#os.environ.get('SLACK_BOT_TOKEN')
slack_clients = slackclient.SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM

###File Path for Questions and Responses
data = pd.read_csv('./dialog_talk_agent.csv')
print(data)
data.ffill(axis=0, inplace= True)
context = data['Context'].values
context_string = data['Context'].str.cat(sep='\n')


## Text Preprocessing
def nltk_cleaning(text):
  token_text = word_tokenize(text)
  clean_text = ["UNK"]
  lemma = wordnet.WordNetLemmatizer()
  tag_list = pos_tag(token_text, tagset=None)
  for token, pos_token in tag_list:
   if token not in '\n\n \n\n\n!"-#$%&()--.*''+,-/:;``<=>[``?@[\\]^_`''{|}~\t\n`\'\'' and (token not in stopwords):
     if pos_token.startswith('V'):  # Verb
         pos_val='v'
     elif pos_token.startswith('J'): # Adjective
         pos_val='a'
     elif pos_token.startswith('R'): # Adverb
         pos_val='r'
     else:
         pos_val='n' # Noun
     lemma_token= lemma.lemmatize(token,pos_val)
     clean_text.append(lemma_token.lower())
   else:
      continue 
  return " ".join(clean_text)
data['nltk_cleaning']= data['Context'].apply(nltk_cleaning)



###bag of words ### TDIF Vectorizer ####
tfidf = TfidfVectorizer() # intializing the count vectorizer
X = tfidf.fit_transform(data['nltk_cleaning']).toarray()
features = tfidf.get_feature_names()
df_idf = pd.DataFrame(X, columns = features)
Question_tf ='thanks for your support!'
Question_lemma_tf = nltk_cleaning(Question_tf) # applying the function that we created for text normalizing
Question_tf = tfidf.transform([Question_lemma_tf]).toarray() # applying bow
cosine_value_tf = 1- pairwise_distances(df_idf, Question_tf, metric = 'cosine' )
index_value = cosine_value_tf.argmax() # returns the index number of highest value
data['similarity_tfidf']=cosine_value_tf # creating a new column
#print(data.sort_values('similarity_tfidf', ascending=False).iloc[0:2])
df_simi_tf = pd.DataFrame(data, columns=['Text Response','similarity_tfidf']) # taking similarity value of responses for the question we took
#print(df_simi_tf.sort_values('similarity_tfidf', ascending=False))
ending_text = ['bye','done', 'thanks', 'exit', 'ok', 'x']


###Parsing the Incoming Commands from Slack

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            message = event["text"]
            return message, event["channel"], event['user']
    return None, None, None

##Looking for direct Mentions


### Generating Response to the Query

def handle_command(command, channel,user):
    # Default response is help text for the user
    accepted_users = [<ACCEPTED SLACK TOKENS FOR AUTHORIZED USERS>]
    ending_text = ['bye','done', 'thanks', 'exit', 'ok', 'x']
    if user not in accepted_users:
          response = "Not an authorised user"
    elif command in ending_text:
          response = "Bye! Thanks for chatting"
    else:
      try:
        Question_lemma_tf = nltk_cleaning(command) # applying the function that we created for text normalizing
        Question_tf = tfidf.transform([Question_lemma_tf]).toarray() # applying bow
        cosine_value_tf = 1- pairwise_distances(df_idf, Question_tf, metric = 'cosine' )
        index_value = cosine_value_tf.argmax()
        response = data['Text Response'].loc[index_value]
      except:
          response='Sorry, Not sure what you mean'
        
    


    # Sends the response back to the channel
    slack_clients.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
       
    )

##Running the application
print("Done")

if __name__ == "__main__":
    if slack_clients.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_clients.api_call("auth.test")["user_id"]
        while True:
            command, channel, user = parse_bot_commands(slack_clients.rtm_read())
            if command == 'shutdownthebot':
                break
            else:
               if command is None:
                  continue
               else:
                  handle_command(command, channel, user)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
