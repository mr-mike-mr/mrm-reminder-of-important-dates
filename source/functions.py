# PACKAGES
try: # try import packages
    # EXTERNAL
    from time import sleep
    from sqlite3 import connect
    from discord_webhook import DiscordWebhook, DiscordEmbed
    from twilio.rest import Client
    from smtplib import SMTP
except ImportError as error: # error handle
    print(f'\n\nModul not installed: {error}\n\n') # print error message + error
    sleep(3600) # sleep 1h
    exit(1)

# SHARED HELP VAR
_ClearCmd = 'cls'

# CONFIG N-TICE
Config = {
    'REFRESH_TIME': 43200,
    'NOTIFY': {'EMAIL':False, 'SMS':False, 'DISCORD':False},
    'SMTP_SERVER': None,'SMTP_PORT': None,'SMTP_EMAIL': None,'SMTP_PASSWORD': None,'SMTP_CLIENT_EMAIL': None,
    'SMS_TOKEN': None,'SMS_SID': None,'SMS_TWILIO_PHONE': None,'SMS_CLIENT_PHONE': None,
    'DISCORD_WEBHOOK': None
}

# ERROR FUNC
def Error(text): # text = error message
    print(f'\n\n{text}\n\nPlease contact support: https://discord.com/invite/mCCj29zSwH / https://github.com/mr-mike-mr/mrm-reminder-of-important-dates\n\n') # error message
    sleep(3600) # wait 1h
    exit(1)

# VERIFY FUNC
def Verify(text):
    while 1:
        value = str(input(text))

        if value == 'Y' or value == 'y': # if value is y/Y then
            return True
        if value == 'N' or value == 'n': # if value is n/N then
            return False
        else:
            print("The answer must be 'Y/n'!\n") # warn message

# DATABASE CONNECT FUNC
def DatabaseConnect():
    try: # try open database
        db_connect = connect('../data/database.db') # call connect func from sqlite3 for connect/open database
        db_cursor = db_connect.cursor() # call cursor func from sqlite3 for rows manipulate
        return [db_connect, db_cursor]
    except: # error handle
        error('Database open failed')

# DATABASE DISCONNECT FUNC
def DatabaseDisconnect(db_connect): # db_connect = sqlite3 connect object
    try: # try close database
        db_connect.close() # call close func from sqlite3 for disconnect/close database
        return True
    except: # error handle
        error('Database close failed')

# EMAIL NOTIFY FUNC
def EmailNotify(title, text): # title = email message title ; text = email message text
    try: # try send email
        with SMTP(Config['SMTP_SERVER'], Config['SMTP_PORT']) as smtp: # call SMTP function from smtplib for initialize a new instance
            smtp.starttls() # call starttls function from smtplib for puts the connection to the SMTP server into TLS mode
            smtp.login(Config['SMTP_EMAIL'], Config['SMTP_PASSWORD']) # call starttls function from smtplib for log in on an SMTP server
            smtp.sendmail(Config['SMTP_EMAIL'], Config['SMTP_CLIENT_EMAIL'], f'Subject: Reminder of Importrant Dates - {title}\n\n{text}') # call starttls function from smtplib for performs an entire mail transaction
        return True
    except: # error handle
        print('Incorrect smtp service values!\n')
        sleep(2)
        return False

# SMS NOTIFY FUNC
def SmsNotify(message): # message = sms message
    try: # try send sms
        client = Client(Config['SMS_SID'], Config['SMS_TOKEN']) # call create func from twilio.rest for initializes the twilio client
        message = client.messages.create( # call create func from twilio.rest for create the MessageInstance
            from_ = Config['SMS_TWILIO_PHONE'], # sender
            body = message, # text content
            to = Config['SMS_CLIENT_PHONE'] # recipient
        )
        return True
    except: # error handle
        print('Incorrect twilio service values!\n')
        sleep(2)
        return False

# DISCORD (WEBHOOK) NOTIFY FUNC
def DiscordNotify(title, text, color): # title = discord message title; text = discord message text; color = discord message color
    try: # try send discord message on webhook
        webhook = DiscordWebhook(url=Config['DISCORD_WEBHOOK'], rate_limit_retry=True) # call DiscordWebhook func from discord_webhook for init discord webhook
        embed = DiscordEmbed(title=title, description=text, color=color) # call DiscordWebhook func from discord_webhook for init discord embed
        embed.set_author(name='Reminder-of-Important-Dates', url='https://github.com/mr-mike-mr/mrm-reminder-of-important-dates') # call DiscordWebhook func from discord_webhook for set information about the author of the embed
        embed.set_footer(text='Created By mr.mike3319') # call DiscordWebhook func from discord_webhook for set footer information in the embed
        webhook.add_embed(embed) # call DiscordWebhook func from discord_webhook for add an embedded rich content
        webhook.execute() # call DiscordWebhook func from discord_webhook for execute the sending of the webhook with the given data
        return True
    except: # error handle
        print('Incorrect discord webhook!\n')
        sleep(2)
        return False