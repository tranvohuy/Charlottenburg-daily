from os import environ

#this is a less secure method. Google auth is better but I don't know how to do it yet.
import smtplib

def send_email(ads_msgs):
    gmail_bot = environ['gmail_bot']
    gmail_bot_pwd = environ['gmail_bot_pwd']

    sent_from = gmail_bot
    to = environ['email_to']  
    print(to)
    subject = 'Charlottenburg new rental ads'  
    body = "\n".join(ads_msgs)
    

    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s

    %s
    """ % (sent_from,  to, subject, body)
    print(email_text)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_bot, gmail_bot_pwd)
        server.sendmail(sent_from, to, email_text.encode())
        server.close()
        print('Email sent.')
    except:
        print('Something went wrong...')
