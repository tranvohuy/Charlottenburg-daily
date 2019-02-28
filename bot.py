import tweepy
from datetime import date
from messages import get_messages
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials


from os import environ
Consumer_key= environ['Consumer_key']
Consumer_secret = environ['Consumer_secret']
Access_key = environ['Access_key']
Access_secret = environ['Access_secret']

json_creds = environ['google_cred']
creds_dict = json.loads(json_creds)



auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_key, Access_secret)
api = tweepy.API(auth)

scopes = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
gc = gspread.authorize(creds)


if __name__=='__main__':
    
    messages = get_messages()

    print("about to update status...")
    try:
         api.update_status(messages)
