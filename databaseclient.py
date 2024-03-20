# TODO: make dokumentation
# TODO: optimalizate
try:
    from os import system
    from time import sleep
    from sqlite3 import Error

    import main
    import config
    import functions

except ImportError as error:
    print(f'\n\nModul not installed: {error}\n\n')
    sleep(60)
    exit(1)

def addDate():
    text = input("\nDate text > ")
    date = dateInput()

    db = functions.databaseConnect()

    print(f'\nAdding a date \'{text}\' - \'{date}\'...')

    try:
        db[1].execute(f"INSERT INTO dates (text, date) VALUES ('{text}','{date}')")
        db[0].commit()
    except Error as error:
        error(f'Add new date into database failed: {error}')

    functions.databaseDisconnect(db[0])

    print(f'Data \'{date} - {text}\' added!')
    sleep(5)

def removeData():
    if functions.verify('Want to remove the date [Y/n]? > '):
        id = functions.numInput('Date id > ')
        db = functions.databaseConnect()

        print(f'\nRemoving a date \'{id}\'...')

        try:
            db[1].execute(f"DELETE from dates where id = {id}")
            db[0].commit()
        except Error as error:
            error(f'Removed date in database failed: {error}')

        functions.databaseDisconnect(db[0])

        print(f'Date \'{id}\' removed!')
        sleep(5)

def dateInput():
    date = [0, 0, 0]

    while 1:
        date[0] = functions.numInput("Day > ")
        if date[0] >= 0 and date[0] <= 31:
            break
        else:
            print("Wrong day!\n")
    while 1:
        date[1] = functions.numInput("Month > ")
        if date[1] >= 0 and date[1] <= 12:
            break
        print("Wrong month!\n")
    date[2] = functions.numInput("Year > ")

    return (f'{date[0]}.{date[1]}.{date[2]}')

def Main():
    while 1:
        system(config.CLEAR_CMD)
        print('### Reminder of Important Dates | DATABASE CLIENT ###')

        print('\n# DATES:')
        db = functions.databaseConnect()
        for row in db[1].execute("SELECT * FROM dates"):
            print(row)
        functions.databaseDisconnect(db[0])

        print('\n# OPTIONS:')
        print('1|Add Date')
        print('2|Remove Date')
        print('3|Back')

        option = functions.numInput('\nSelect option > ')

        if option == 1:
            addDate()
        elif option == 2:
            removeData()
        elif option == 3:
            if functions.verify('Want to go back [Y/n]? > '):
                main.panel()
        else:
            print('Wrong option!')
            sleep(2)