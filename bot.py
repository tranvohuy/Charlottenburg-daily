import tweepy
from datetime import date
from messages import get_messages
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

import gspread_dataframe as gsdf
from immo import immosearch

from os import environ
Consumer_key= environ['Consumer_key']
Consumer_secret = environ['Consumer_secret']
Access_key = environ['Access_key']
Access_secret = environ['Access_secret']




auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_key, Access_secret)
api = tweepy.API(auth)

ddef get_client():
    scopes = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    json_creds = environ['google_cred']
    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    gc = gspread.authorize(creds)
    return gc


if __name__=='__main__':
    gc = get_client()
    sh = gc.open('Berlin-rental')
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d')
    df = immosearch()


    print("about to update status...")
    try:
         api.update_status(messages)
