from os import environ
'''
smtplib is a less secure method than google auth. 
To use google auth, see https://github.com/shankarj67/python-gmail-api
'''
import smtplib

def send_email(ads_msgs):
    gmail_bot = environ['gmail_bot']
    gmail_bot_pwd = environ['gmail_bot_pwd']

    sent_from = gmail_bot
    
    to = environ['email_to']
    to = to.replace(',',' ')
    
    #to is a list of emails.
    #to = ['user1@amail.com', 'user2@bmail.com']
    to = to.split()
    
    '''
    Example for the value in 'email_to': 'user1@amail.com, user2@gmai.com'
    Each email is separated by a commas ','. Blank spaces are allowed
    'user1@amail.com,     user2@gmai.com' is also valid
    'user1@gmail.com,    user2@dkjf.com' is also valid
    'user1@gmail.com,    user2@dkjf.com,' is also valid
    '''
    
    
    print(to)
    subject = 'Charlottenburg new rental ads'  
    body = "\n".join(ads_msgs)
    

    email_text = """Subject:%s\n\n  %s""" % (subject, body)
    print(email_text)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_bot, gmail_bot_pwd)
        server.sendmail(sent_from, to, email_text.encode())
        server.close()
        print('Email sent.')
    except Exception as e:
        print('Something went wrong with emails: ', e)
