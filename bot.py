import tweepy
from datetime import date
from immo import immosearchnew
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

import gspread_dataframe as gsdf
import pandas as pd
from os import environ

from send_email import send_email


def get_client():
    scopes = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    json_creds = environ['google_cred']
    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    gc = gspread.authorize(creds)
    return gc

def update_tweet(ads_msgs):
    consumer_key= environ['consumer_key']
    consumer_secret = environ['consumer_secret']
    access_key = environ['access_key']
    access_secret = environ['access_secret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    status = ads_msgs[0]
    
    if len(ads_msgs)==1:
        api.update_status(status)
    else:
        for i in range(1,len(ads_msgs)):
            status_temp = status + '\n' + ads_msgs[i]
            if (len(status_temp)>280):
                api.update_status(status)
                status = '(cont.)\n' + ads_msgs[i]
            else:
                status = status_temp
        if len(status)>0:
            api.update_status(status)


def create_twitter_msgs(df_new):
    if df_new.shape[0]==0:
        return ['No new ads in Charlottenburg today.']
    msgs = ['%s new ads in #Charlottenburg today' %(df_new.shape[0])]
    for index, row in df_new.iterrows():
        msgs.append( '(cold)%s€, (warm)%s€, %srooms, %sm²→ %s' %(row['price'], row['warmprice'], \
                                                                  row['numberOfRooms'], row['livingSpace'], row['url']))
    return msgs
    
def create_email_msg(df_new):
    msg = ['%s new ads in Charlottenburg today' %(df_new.shape[0])]
    if df_new.shape[0]==0:
        return msg
    for index, row in df_new.iterrows():
       # print(row['privateOffer'])
       # print(type(row['privateOffer']))
        msg.append( '%s€/%s€, %sR, %sm², private(%s), kitchen(%s), balcony(%s)→ %s' %(row['price'], row['warmprice'], \
                                                                  row['numberOfRooms'], row['livingSpace'], \
                                                                    'Y' if row['privateOffer']=='true' else 'N', \
                                                                    'Y' if row['builtInKitchen']=='true' else 'N',\
                                                                    'Y' if row['balcony']=='true' else 'N',\
                                                                      row['url']))
    return msg  
#---main program----
if __name__=='__main__':

    gc = get_client()
    wks = gc.open('Charlottenburg').sheet1

    df_old = gsdf.get_as_dataframe(wks)
    #a list of old id
    if df_old.shape[0]!=0:
        old_ids = df_old['ID'].unique()
    else: #there is no ads in gsheet file, this is for the first time running the program
        old_ids = []


    [df_new, ids_keep] = immosearchnew(old_ids)
    if df_new.shape[0]!=0:
        df_new = df_new.sort_values(by=['numberOfRooms', 'warmprice'])
    print('ready to tweet')
    twitter_msgs = create_twitter_msgs(df_new)
    print(twitter_msgs)
    #update_tweet(twitter_msgs)
    
    email_msg = create_email_msg(df_new)
    print(email_msg)
    #send_email(email_msg)
            
    if df_new.shape[0]==0:
      exit()

    #-----now save to the file------
  #  df_keep = df_old[df_old['ID'].isin(ids_keep)]
  #  print('Delete {} old ads'.format(df_old.shape[0] - df_keep.shape[0]))
  #  frame = [df_new, df_keep]
  #  df = pd.concat(frame, ignore_index = True)
   # df.index.name = 'ID'

    
   # gsdf.set_with_dataframe(wks, df, resize = True)
