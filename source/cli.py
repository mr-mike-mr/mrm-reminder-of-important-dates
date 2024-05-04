# PACKAGES
try: # try import packages
    # EXTERNAL
    from os import system
    from time import sleep
    from json import dumps
    import subprocess
    import sys
    # OWN
    import functions
except ImportError as error: # error handle
    print(f'\n\nModul not installed: {error}\n\n') # print error message + error
    sleep(3600) # sleep 1h
    exit(1)

# NUMBER INPUT FUNC
def num_input(text = None, value = None): # text = input text for cli version ; value = value to check for gui versions
    # CLI VERSION
    while 1:
        try: # try convert input to int
            value = int(input(text))
            return value
        except: # error handle
            print('Input must be number!\n')

# SAVE CONFIG FUNC
def save_config():
    try: # try dump and save config
        ConfigJson = dumps(functions.Config) # call dumps function from json for serialize object to a json formatted string
        with open("../data/config.json", "w") as config_file: # opens config.json file and return a stream
            config_file.write(ConfigJson) # call dumps function from json for write ConfigJson into config.json
            print("Config save successful!\n")
            return True
    except: # error handle
        functions.error('Config save failed')

# ADD DATE (FOR DATABASE) FUNC
def add_date(text, date, warn_date): # text = text for insert into database ; date = date for insert into database ; warn_date = warn date for insert into database
    db = functions.DatabaseConnect() # call DatabaseConnect func for connect/open database

    try: # try insert data into database.db for Dates table
        db[1].execute("INSERT INTO Dates (text, date, `warn_date`) VALUES (?, ?, ?)", (text, date, warn_date)) # call execute func from sqlite3 for run insert sql query
        db[0].commit() # call commit func from sqlite3 for confirm change
    except: # error handle
        error('Add new date into database failed')

    functions.DatabaseDisconnect(db[0]) # call DatabaseDisconnect func for disconnect/close database
    return True

# REMOVE DATE (FOR DATABASE) FUNC
def remove_data(id): # id = to remove from database
    db = functions.DatabaseConnect() # call DatabaseConnect func for connect/open database

    try: # try remove data from database.db for Dates table
        db[1].execute(f"DELETE from Dates where id = {id}") # call execute func from sqlite3 for run delete sql query
        db[0].commit() # call commit func from sqlite3 for confirm change
    except: # error handle
        error('Removed date in database failed')

    functions.DatabaseDisconnect(db[0]) # call DatabaseDisconnect func for disconnect/close database
    return True

# CLI DATABASE CLIENT FUNC
def cli_databaseclient():
    # DATA INPUT FUNC
    def _date_input(day_input, month_input, year_input):
        # DAY
        while 1:
            day = num_input(f"{day_input} > ") # call num_input for number value
            if day >= 0 and day <= 31: # if day more or equal to 0 and less or equal to 31 then
                break
            else:
                print("Wrong day!\n")
        # MONTH
        while 1:
            month = num_input(f"{month_input} > ") # call num_input for number value
            if month >= 0 and month <= 12: # if month more or equal to 0 and less or equal to 12 then
                break
            print("Wrong month!\n")
        # YEAR
        year = num_input(f"{year_input} > ") # call num_input for number value

        return f'{day}.{month}.{year}' # return formatted date

    # MAIN
    while 1:
        # TITLE
        system(functions._ClearCmd) # get clear command from _ClearCmd from functions.py and clear consol
        print('### Reminder of Important Dates | DATABASE CLIENT ###')

        # SHOW DATES
        print('\n# DATES:')
        db = functions.DatabaseConnect() # call DatabaseConnect func from functions.py for connect/open database and save database objects
        for row in db[1].execute("SELECT * FROM dates"): # goes through all rows in the database
            print(f'{row[0]} | {row[1]} | {row[2]} | {row[3]}') # 'row[id] | row[text] | row[date] | row[warn_date]'
        functions.DatabaseDisconnect(db[0]) # call DatabaseDisconnect func from functions.py for disconnect/close database

        # OPTIONS
        print('\n# OPTIONS:')
        print('1|Add Date')
        print('2|Remove Date')
        print('3|Back')
        option = num_input('\nSelect option > ') # call num_input for number value

        # OPTION CONDITION
        if option == 1: # if option is 1 then
            if functions.Verify('Want to add a date [Y/n]? > '): # if return value from Verify func from functions.py is true then
                text = input("\nDate text > ")
                date = _date_input('Day', 'Month', 'Year') # call _date_input for date value
                warn_date = _date_input('Warn day', 'Warn month', 'Warn year') # call _date_input func for date value

                print(f"Adding a date '{text}' - '{date} ({warn_date})'...")
                add_date(text, date, warn_date) # call AddDate func from functions.py for add date into database
                print(f"Data '{date} - {text}' added!")
                sleep(2)
        elif option == 2: # if option is 2 then
            if functions.Verify('Want to remove the date [Y/n]? > '): # if return value from Verify func from functions.py is true then
                id = num_input('\nDate id > ') # call num_input for number value

                print(f"Removing a date '{id}'...")
                remove_data(id) # call RemoveData func from functions.py for remove date from database
                print(f"Date '{id}' removed!")
                sleep(2)
        elif option == 3: # if option is 3 then
            if functions.Verify('Want to go back [Y/n]? > '): # if return value from Verify func from functions.py is true then
                CliPanel() # call CliPanel func for return to panel
        else:
            print('Wrong option!')
            sleep(2)

# CLI CONFIG FUNC
def cli_config():
    # TITLE
    system(functions._ClearCmd) # get clear command from _ClearCmd from functions.py and clear consol
    print('### Reminder of Important Dates | CONFIG ###')

    # CONFIG
    functions.Config['REFRESH_TIME'] = num_input('\nEnter server refresh time [hod.]? > ') * 3600 # call num_input for number value, convert from seconds to hours and save into Config['SMTP_PORT'] from functions.py
    # EMAIL CONFIG
    if functions.Verify('\nWant email notifications [Y/n]? > '): # if return value from Verify func from functions.py is true then
        while 1:
            # INPUTS
            functions.Config['SMTP_SERVER'] = str(input('Enter smtp server > ')) # get input and save into Config['SMTP_SERVER'] from functions.py
            functions.Config['SMTP_PORT'] = num_input('Enter smtp port > ') # call num_input for number value and save into Config['SMTP_PORT'] from functions.py
            functions.Config['SMTP_EMAIL'] = str(input('Enter smtp email > ')) # get input and save into Config['SMTP_EMAIL'] from functions.py
            functions.Config['SMTP_PASSWORD'] = str(input('Enter smtp password > ')) # get input and save into Config['SMTP_PASSWORD'] from functions.py
            functions.Config['SMTP_CLIENT_EMAIL'] = str(input('Enter your email > ')) # get input and save into Config['SMTP_CLIENT_EMAIL'] from functions.py
            # TEST
            if functions.EmailNotify('TEST', 'test notify') and functions.Verify('Did you get the test message [Y/n]? > '): # if return value from EmailNotify and Verify funcs from functions.py is true then
                functions.Config['NOTIFY']['EMAIL'] = True # change value in Config['NOTIFY']['EMAIL'] in functions.py
                break
    # SMS CONFIG
    if functions.Verify('\nDo you want SMS notifications [Y/n]? > '): # if return value from Verify func from functions.py is true then
        while 1:
            # INPUTS
            functions.Config['SMS_TOKEN'] = str(input('Enter twilio token > ')) # get input and save into Config['SMS_TOKEN'] from functions.py
            functions.Config['SMS_SID'] = str(input('Enter twilio sid > ')) # get input and save into Config['SMS_SID'] from functions.py
            functions.Config['SMS_TWILIO_PHONE'] = str(input('Enter twilio phone number [format: +123456789] > ')) # get input and save into Config['SMS_TWILIO_PHONE'] from functions.py
            functions.Config['SMS_CLIENT_PHONE'] = str(input('Enter yout phone number [format: +123456789] > ')) # get input and save into Config['SMS_CLIENT_PHONE'] from functions.py
            # TEST
            if functions.SmsNotify('test notify') and functions.Verify('Did you get the test message [Y/n]? > '): # if return value from SmsNotify and Verify funcs from functions.py is true then
                functions.Config['NOTIFY']['SMS'] = True # change value in Config['NOTIFY']['SMS'] in functions.py
                break
    # DISCORD CONFIG
    if functions.Verify('\nDo you want notifications on the discord server [Y/n]? > '): # if return value from Verify func from functions.py is true then
        while 1:
            functions.Config['DISCORD_WEBHOOK'] = str(input('Enter discord webhook > ')) # get input and save into Config['DISCORD_WEBHOOK'] from functions.py
            # TEST
            if functions.DiscordNotify('TEST', 'test notify', 'eb8e02') and functions.Verify('Did you get the test message [Y/n]? > '): # if return value from DiscordNotify and Verify funcs from functions.py is true then
                functions.Config['NOTIFY']['DISCORD'] = True # change value in Config['NOTIFY']['DISCORD'] in functions.py
                break

    save_config() # call save_config for save config
    CliPanel() # call CliPanel func for return to panel

# CLI PANEL FUNC
def CliPanel():
    while 1:
        # TITLE
        system(functions._ClearCmd) # get clear command from _ClearCmd from functions.py and clear consol
        print('### Reminder of Important Dates | PANEL ###')

        # OPTIONS
        print('\n# OPTIONS:')
        print('1|Database Client')
        print('2|Config')
        print('3|Server')
        print('4|Exit')
        option = num_input('\nSelect option > ') # call num_input number input

        # OPTION CONDITION
        if option == 1: # if option is 1 then
            if functions.Verify('Want to use a database client [Y/n]? > '): # if return value from Verify func from functions.py is true then
                cli_databaseclient()
        elif option == 2: # if option is 2 then
            if functions.Verify('Want to configure [Y/n]? > '): # if return value from Verify func from functions.py is true then
                cli_config()
        elif option == 3: # if option is 3 then
            if functions.Verify('Want to start a server [Y/n]? > '): # if return value from Verify func from functions.py is true then
                system(functions._ClearCmd) # get clear command from _ClearCmd from functions.py and clear consol
                subprocess.Popen(['python', 'server.py']) # run server.py as a subprocess
                sys.exit() # exit from cli.py
        elif option == 4: # if option is 4 then
            if functions.Verify('Want to exit [Y/n]? > '): # if return value from Verify func from functions.py is true then
                exit(1)
        else:
            print('Wrong option!')
            sleep(2)