# PACKAGES
try: # try import packages
    # EXTERNAL
    from time import sleep
    from datetime import datetime
    from json import load
    # OWN
    import functions
except ImportError as error: # error handle
    print(f'\n\nModul not installed: {error}\n\n') # print error message + error
    sleep(3600) # sleep 1h
    exit(1)

# CONFIG LOAD
try: # try load config
    with open("../data/config.json", "r") as configFile: # opens config.json file and return a stream
        functions.Config = load(configFile) # load data from config.json and save into Config n-tice in main.py
except: # error handle
    sleep(3)

# HELP VARS
id = 1
current_date = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}' # call datetime func from datetime for get current date
current_time = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}' # call datetime func from datetime for get current time

# CHECKER AND CONSOL LOG
while True:
    current_date = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}' # call datetime func from datetime for get current date
    current_time = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}' # call datetime func from datetime for get current time
    db = functions.DatabaseConnect() # call DatabaseConnect func from functions.py for connect/open database

    for row in db[1].execute("SELECT * FROM Dates"): # goes through all rows in the database table
        # MATCH
        if row[2] == current_date: # if date is current_date then
            # EMAIL NOTIFY
            if functions.Config['NOTIFY']['EMAIL']: # if Config['NOTIFY']['EMAIL'] from functions.py is true then
                functions.EmailNotify('MATCH', f'MATCH | {row[1]} | {current_date} | {current_time}') # call EmailNotify func for send notify to email
            # SMS NOTIFY
            if functions.Config['NOTIFY']['SMS']: # if Config['NOTIFY']['SMS'] from functions.py is true then
                functions.SmsNotify(f'MATCH | {row[1]} | {current_date} | {current_time}') # call SmsNotify func for send notify to sms
            # DISCORD NOTIFY
            if functions.Config['NOTIFY']['DISCORD']: # if Config['NOTIFY']['DISCORD'] from functions.py is true then
                functions.DiscordNotify('MATCH', f'{row[1]} | {current_date} | {current_time}', '0bfc03') # call DiscordNotify func for send notify to discord
            id += 1
        # MATCH WARN
        elif row[3] == current_date: # if warn_date is current_date then
            # EMAIL NOTIFY
            if functions.Config['NOTIFY']['EMAIL']: # if Config['NOTIFY']['EMAIL'] from functions.py is true then
                functions.EmailNotify('MATCH WARN', f'MATCH WARN | {row[1]} - {row[2]} | {current_date} | {current_time}') # call EmailNotify func from functions.py for send notify to email
            # SMS NOTIFY
            if functions.Config['NOTIFY']['SMS']: # if Config['NOTIFY']['SMS'] is true then
                functions.SmsNotify(f'MATCH WARN | {row[1]} - {row[2]} | {current_date} | {current_time}') # call SmsNotify func from functions.py for send notify to sms
            # DISCORD NOTIFY
            if functions.Config['NOTIFY']['DISCORD']: # if Config['NOTIFY']['DISCORD'] is true then
                functions.DiscordNotify('MATCH WARN', f'{row[1]} - {row[2]} | {current_date} | {current_time}', '0bfc03') # call DiscordNotify func from functions.py for send notify to discord
            id += 1

    # END OF CYCLE
    functions.DatabaseDisconnect(db[0]) # call DatabaseDisconnect func from functions.py for disconnect/close database
    sleep(functions.Config['REFRESH_TIME']) # get refresh time from Config['REFRESH_TIME'] from functions.py for server wait