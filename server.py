# TODO: make dokumentation
# TODO: optimalizate
try:
    from os import system
    from time import sleep
    from sqlite3 import Error
    from datetime import datetime

    import config
    import functions

except ImportError as error:
    print(f'\n\nModul not installed: {error}\n\n')
    sleep(60)
    exit(1)

def Main():
    system(config.CLEAR_CMD)
    print('### Reminder of Important Dates | SERVER [CTRL+C FOR STOP] ###')
    print('# CONFIG:')
    print(f'Refresh time > {config.Config['REFRESH_TIME']}')
    print(f'Notify > {config.Config['NOTIFY']}')
    if config.Config['NOTIFY']['EMAIL']:
        print(f'Smtp server > {config.Config['SMTP_SERVER']}')
        print(f'Smtp port > {config.Config['SMTP_PORT']}')
        print(f'Smtp email > {config.Config['SMTP_EMAIL']}')
        print(f'Client email > {config.Config['CLIENT_EMAIL']}')
    if config.Config['NOTIFY']['SMS']:
        print(f'Twilio token > {config.Config['SMS_TOKEN'][:10]}')
        print(f'Twilio sid > {config.Config['SMS_SID'][:10]}')
        print(f'Twilio phone > {config.Config['SMS_TWILIO_PHONE']}')
        print(f'Client phone > {config.Config['SMS_CLIENT_PHONE']}')
    if config.Config['NOTIFY']['DISCORD']:
        print(f'Discord webhook > {config.Config['DISCORD_WEBHOOK'][24:52]}')

    print('LOG | Reminder of Important Date start!')
    id = 1
    while 1:
        print('\n# LOG CONSOLE:')

        current_date = f'{datetime.now().day}.{datetime.now().month}.{datetime.now().year}'
        current_time = f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'

        db = functions.databaseConnect()
        for row in db[1].execute("SELECT text, date FROM dates"):
            if row[1] == current_date:
                print(f'\nLOG | {id} | Match | {row[0]} | {current_date} - {current_time}')

                if config.Config['NOTIFY']['EMAIL']:
                    print(f'LOG | {id} | Sending email | {row[0]} | {current_date} - {current_time}')
                    functions.emailNotify('MATCH', f'MATCH | {row[0]} | {current_date} | {current_time}')
                    print(f'LOG | {id} | Email sent | {row[0]} | {current_date} - {current_time}')

                if config.Config['NOTIFY']['SMS']:
                    print(f'LOG | {id} | Sending sms | {row[0]} | {current_date} - {current_time}')
                    functions.smsNotify(f'MATCH | {row[0]} | {current_date} | {current_time}')
                    print(f'LOG | {id} | Sms sent | {row[0]} | {current_date} - {current_time}')

                if config.Config['NOTIFY']['DISCORD']:
                    print(f'LOG | {id} | Sending message on discord | {row[0]} | {current_date} - {current_time}')
                    functions.discordNotify('MATCH', f'{row[0]} | {current_date} | {current_time}', '0bfc03')
                    print(f'LOG | {id} | Message on discord sent | {row[0]} | {current_date} - {current_time}')

                id =+ 1
        functions.databaseDisconnect(db[0])

        sleep(config.Config['REFRESH_TIME'])