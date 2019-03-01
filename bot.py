import tweepy
from datetime import date
from immo import immosearchnew
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

import gspread_dataframe as gsdf

from os import environ





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

def update_tweet(df_new):
    consumer_key= environ['consumer_key']
    consumer_secret = environ['consumer_secret']
    access_key = environ['access_key']
    access_secret = environ['access_secret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    if df_new.shape[0] == 0:
      api.update_status('No new ads in Charlottenburg today.')
    else:
      msg = '%s new ads in Charlottenburg today' %(df_new.shape[0])
      
      count = 0
      for index, row in df_new.iterrows():
        msg = msg + '\n' + '(cold)%s€, (warm)%s€, %s rooms, %sm²->%s' %(row['price'], row['warmprice'], \
                                                                  row['numberOfRooms'], row['area'], row['url'])
        count +=1
        if count ==3:
          count ==0
          print(msg)
          api.update_status(msg)
          msg ='(cont.)'
      if count>0:
        api.update_status(msg) 

      
#---main program----
if __name__=='__main__':

    gc = get_client()
    wks = gc.open('Charlottenburg').sheet1

    df_old = gsdf.get_as_dataframe(wks)
    #a list of old id
    old_ids = df_old['ID'].unique()


    df_new = immosearchnew(old_ids)
    print('ready to tweet')
    update_tweet(df_new)
    if df_new.shape[0]==0:
      exit()

    #-----now save to the file------
    frame = [df_new, df_old]
    df = pd.concat(frame, ignore_index = True)
    df.index.name = 'ID'

    
    gsdf.set_with_dataframe(wks, df, resize = True)
