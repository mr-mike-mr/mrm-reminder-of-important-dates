# PACKAGES
try: # try import packages
    # EXTERNAL
    from time import sleep
    from sqlite3 import connect
    from discord_webhook import DiscordWebhook, DiscordEmbed
    from twilio.rest import Client
    from smtplib import SMTP
    from tkinter import messagebox
    from json import dumps
    from tkinter import Label
    from datetime import datetime
    from os import system
except ImportError as error: # error handle
    print(f'\n\nModul not installed: {error}\n\n') # print error message + error
    sleep(3600) # sleep 1h
    exit(1)

# SHARED HELP VAR
_ClearCmd = 'cls'
_Version = 'cli'
_ServerStatus = False

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
    # CLI VERSION
    if _Version == 'cli': # if _Version is cli then
        print(f'\n\n{text}\n\nPlease contact support: https://discord.com/invite/SK8Z3uV72k / https://github.com/mr-mike-mr/mrm-reminder-of-important-dates\n\n') # error message
    # GUI VERSION
    else:
        messagebox.showerror('Error', f'{text}\nPlease contact support: https://discord.com/invite/SK8Z3uV72k / https://github.com/mr-mike-mr/mrm-reminder-of-important-dates') # show tkinter error messagebox
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

# NUMBER INPUT FUNC
def NumInput(text = None, value = None): # text = input text for cli version ; value = value to check for gui versions
    # CLI VERSION
    if _Version == 'cli':
        while 1:
            try: # try convert input to int
                value = int(input(text))
                return value
            except: # error handle
                print('Input must be number!\n')
    # GUI VERSION
    else:
        if str.isdigit(value): # if value is int/flow then
            return True
        else:
            messagebox.showwarning('Input', 'Input must be number!') # show tkinter warning messagebox
            return False

# DATABASE CONNECT FUNC
def DatabaseConnect():
    try: # try open database
        db_connect = connect('data/database.db') # call connect func from sqlite3 for connect/open database
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

# ADD DATE (FOR DATABASE) FUNC
def AddDate(text, date, warn_date): # text = text for insert into database ; date = date for insert into database ; warn_date = warn date for insert into database
    db = DatabaseConnect() # call DatabaseConnect func for connect/open database

    try: # try insert data into database.db for Dates table
        db[1].execute("INSERT INTO Dates (text, date, `warn_date`) VALUES (?, ?, ?)", (text, date, warn_date)) # call execute func from sqlite3 for run insert sql query
        db[0].commit() # call commit func from sqlite3 for confirm change
    except: # error handle
        error('Add new date into database failed')

    DatabaseDisconnect(db[0]) # call DatabaseDisconnect func for disconnect/close database
    return True

# REMOVE DATE (FOR DATABASE) FUNC
def RemoveData(id): # id = to remove from database
    db = DatabaseConnect() # call DatabaseConnect func for connect/open database

    try: # try remove data from database.db for Dates table
        db[1].execute(f"DELETE from Dates where id = {id}") # call execute func from sqlite3 for run delete sql query
        db[0].commit() # call commit func from sqlite3 for confirm change
    except: # error handle
        error('Removed date in database failed')

    DatabaseDisconnect(db[0]) # call DatabaseDisconnect func for disconnect/close database
    return True

# EMAIL NOTIFY FUNC
def EmailNotify(title, text): # title = email message title ; text = email message text
    try: # try send email
        with SMTP(Config['SMTP_SERVER'], Config['SMTP_PORT']) as smtp: # call SMTP function from smtplib for initialize a new instance
            smtp.starttls() # call starttls function from smtplib for puts the connection to the SMTP server into TLS mode
            smtp.login(Config['SMTP_EMAIL'], Config['SMTP_PASSWORD']) # call starttls function from smtplib for log in on an SMTP server
            smtp.sendmail(Config['SMTP_EMAIL'], Config['SMTP_CLIENT_EMAIL'], f'Subject: Reminder of Importrant Dates - {title}\n\n{text}') # call starttls function from smtplib for performs an entire mail transaction
        return True
    except: # error handle
        # CLI VERSION
        if _Version == 'cli':
            print('Incorrect smtp service values!\n')
            sleep(2)
        # GUI VERSION
        else:
            messagebox.showwarning('Smtp', 'Incorrect smtp service values!') # show tkinter warning messagebox
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
        # CLI VERSION
        if _Version == 'cli':
            print('Incorrect twilio service values!\n')
            sleep(2)
        # GUI VERSION
        else:
            messagebox.showwarning('Twilio', 'Incorrect twilio service values!') # show tkinter warning messagebox
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
        # CLI VERSION
        if _Version == 'cli':
            print('Incorrect discord webhook!\n')
            sleep(2)
        # GUI VERSION
        else:
            messagebox.showwarning('Discord', 'Incorrect discord webhook!') # show tkinter warning messagebox
        return False

# SAVE CONFIG FUNC
def SaveConfig():
    try: # try dump and save config
        ConfigJson = dumps(Config) # call dumps function from json for serialize object to a json formatted string
        with open("data/config.json", "w") as config_file: # opens config.json file and return a stream
            config_file.write(ConfigJson) # call dumps function from json for write ConfigJson into config.json
            # CLI VERSION
            if _Version == 'cli':
                print("Config save successful!\n")
            # GUI VERSION
            else:
                messagebox.showinfo('Config', 'Config save successful!') # show tkinter info messagebox
            return True
    except: # error handle
        error('Config save failed')

# SERVER
def Server(frame=None): # frame = tkinter frame
    # MESSAGE FUNC
    def _message(text): # text = text for show ; frame = tkinter frame
        # CLI VERSION
        if _Version == 'cli': # if _Version is cli
            print(text)
        # GUI VERSION
        else:
            Label(frame, text=text, pady=0, padx=0, font=6).pack(fill='none') # call Lable func from tkinter for construct a label widget with the parent frame

    # HELP VARS
    id = 1
    current_date = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}' # call datetime func from datetime for get current date
    current_time = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}' # call datetime func from datetime for get current time

    # CONFIG
    _message('# CONFIG TEST:')
    _message(f'Refresh time > {Config['REFRESH_TIME']}')
    _message(f'Notify > {Config['NOTIFY']}')

    # EMAIL NOTIFY CONFIG
    if Config['NOTIFY']['EMAIL']: # if Config['NOTIFY']['EMAIL'] is true then
        _message(f'Smtp server > {Config['SMTP_SERVER']}')
        _message(f'Smtp port > {Config['SMTP_PORT']}')
        _message(f'Smtp email > {Config['SMTP_EMAIL']}')
        _message(f'Client email > {Config['SMTP_CLIENT_EMAIL']}')
    # SMS NOTIFY CONFIG
    if Config['NOTIFY']['SMS']: # if Config['NOTIFY']['SMS'] is true then
        _message(f'Twilio token > {Config['SMS_TOKEN'][:10]}')
        _message(f'Twilio sid > {Config['SMS_SID'][:10]}')
        _message(f'Twilio phone > {Config['SMS_TWILIO_PHONE']}')
        _message(f'Client phone > {Config['SMS_CLIENT_PHONE']}')
    # DISCORD NOTIFY CONFIG
    if Config['NOTIFY']['DISCORD']: # if Config['NOTIFY']['DISCORD'] is true then
        _message(f'Discord webhook > {Config['DISCORD_WEBHOOK'][24:52]}')

    # START LOG
    _message('\n# LOG CONSOLE (Exit for stop the server):')

    # CHECKER AND CONSOL LOG
    while True if _Version == 'cli' else _ServerStatus: # if _Version is cli then True, else get value from _ServerStatus variable
        current_date = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}' # call datetime func from datetime for get current date
        current_time = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}' # call datetime func from datetime for get current time
        db = DatabaseConnect() # call DatabaseConnect func for connect/open database

        for row in db[1].execute("SELECT * FROM Dates"): # goes through all rows in the database table
            # MATCH
            if row[2] == current_date: # if date is current_date then
                _message(f'\nLOG | {id} | Match | {row[1]} | {current_date} - {current_time}')
                # EMAIL NOTIFY
                if Config['NOTIFY']['EMAIL']: # if Config['NOTIFY']['EMAIL'] is true then
                    _message(f'LOG | {id} | Sending email | {row[1]} | {current_date} - {current_time}')
                    EmailNotify('MATCH', f'MATCH | {row[1]} | {current_date} | {current_time}') # call EmailNotify func for send notify to email
                    _message(f'LOG | {id} | Email sent | {row[1]} | {current_date} - {current_time}')
                # SMS NOTIFY
                if Config['NOTIFY']['SMS']: # if Config['NOTIFY']['SMS'] is true then
                    _message(f'LOG | {id} | Sending sms | {row[1]} | {current_date} - {current_time}')
                    SmsNotify(f'MATCH | {row[1]} | {current_date} | {current_time}') # call SmsNotify func for send notify to sms
                    _message(f'LOG | {id} | Sms sent | {row[1]} | {current_date} - {current_time}')
                # DISCORD NOTIFY
                if Config['NOTIFY']['DISCORD']: # if Config['NOTIFY']['DISCORD'] is true then
                    _message(f'LOG | {id} | Sending message on discord | {row[1]} | {current_date} - {current_time}')
                    DiscordNotify('MATCH', f'{row[1]} | {current_date} | {current_time}', '0bfc03') # call DiscordNotify func for send notify to discord
                    _message(f'LOG | {id} | Message on discord sent | {row[1]} | {current_date} - {current_time}')
                id += 1
            # MATCH WARN
            elif row[3] == current_date: # if warn_date is current_date then
                _message(f'\nLOG | {id} | MATCH WARN | {row[1]} - {row[2]} | {current_date} - {current_time}')
                # EMAIL NOTIFY
                if Config['NOTIFY']['EMAIL']: # if Config['NOTIFY']['EMAIL'] is true then
                    _message(f'LOG | {id} | Sending email | {row[1]} - {row[2]} | {current_date} - {current_time}')
                    EmailNotify('MATCH WARN', f'MATCH WARN | {row[1]} - {row[2]} | {current_date} | {current_time}') # call EmailNotify func for send notify to email
                    _message(f'LOG | {id} | Email sent | {row[1]} - {row[2]} | {current_date} - {current_time}')
                # SMS NOTIFY
                if Config['NOTIFY']['SMS']: # if Config['NOTIFY']['SMS'] is true then
                    _message(f'LOG | {id} | Sending sms | {row[1]} - {row[2]} | {current_date} - {current_time}')
                    SmsNotify(f'MATCH WARN | {row[1]} - {row[2]} | {current_date} | {current_time}') # call SmsNotify func for send notify to sms
                    _message(f'LOG | {id} | Sms sent | {row[1]} - {row[2]} | {current_date} - {current_time}')
                # DISCORD NOTIFY
                if Config['NOTIFY']['DISCORD']: # if Config['NOTIFY']['DISCORD'] is true then
                    _message(f'LOG | {id} | Sending message on discord | {row[1]} - {row[2]} | {current_date} - {current_time}')
                    DiscordNotify('MATCH WARN', f'{row[1]} - {row[2]} | {current_date} | {current_time}', '0bfc03') # call DiscordNotify func for send notify to discord
                    _message(f'LOG | {id} | Message on discord sent | {row[1]} - {row[2]} | {current_date} - {current_time}')
                id += 1

        # END OF CYCLE
        DatabaseDisconnect(db[0]) # call DatabaseDisconnect func for disconnect/close database
        sleep(Config['REFRESH_TIME']) # get refresh time from Config['REFRESH_TIME'] for server wait