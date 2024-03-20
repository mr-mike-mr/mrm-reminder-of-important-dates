# TODO: make dokumentation
# TODO: optimalizate
try:
    from os import system
    from time import sleep
    from json import dumps

    import main
    import functions

except ImportError as error:
    print(f'\n\nModul not installed: {error}\n\n')
    sleep(60)
    exit(1)

CLEAR_CMD = 'cls'

Config = {
    'REFRESH_TIME': 43200,
    'NOTIFY': {'EMAIL':'false', 'SMS':'false', 'DISCORD':'false'},
    'SMTP_SERVER': None,'SMTP_PORT': None,'SMTP_EMAIL': None,'SMTP_PASSWORD': None,'CLIENT_EMAIL': None,
    'SMS_TOKEN': None,'SMS_SID': None,'SMS_TWILIO_PHONE': None,'SMS_CLIENT_PHONE': None,
    'DISCORD_WEBHOOK': None
}

def Main():
    while 1:
        system(CLEAR_CMD)
        print('### Reminder of Important Dates | CONFIG ###')
        Config['REFRESH_TIME'] = functions.numInput('\nWhen does the server check dates [hod.]? > ') * 3600

        if functions.verify('\nWant email notifications [Y/n]? > '):
            while 1:
                Config['SMTP_SERVER'] = str(input('Enter smtp server > '))
                Config['SMTP_PORT'] = functions.numInput('Enter smtp port > ')
                Config['SMTP_EMAIL'] = str(input('Enter smtp email > '))
                Config['SMTP_PASSWORD'] = str(input('Enter smtp password > '))
                Config['CLIENT_EMAIL'] = str(input('Enter your email > '))
                functions.emailNotify('TEST', 'test notify')
                sleep(1)
                if functions.verify('Did you get the test message [Y/n]? > '):
                    Config['NOTIFY']['EMAIL'] = 'true'
                    break

        if functions.verify('\nDo you want SMS notifications [Y/n]? > '):
            while 1:
                Config['SMS_SID'] = str(input('Enter twilio sid > '))
                Config['SMS_TOKEN'] = str(input('Enter twilio token > '))
                Config['SMS_TWILIO_PHONE'] = str(input('Enter twilio phone number [format: +123456789] > '))
                Config['SMS_CLIENT_PHONE'] = str(input('Enter yout phone number [format: +123456789] > '))
                sleep(1)
                functions.smsNotify('test notify')
                if functions.verify('Did you get the test message [Y/n]? > '):
                    Config['NOTIFY']['SMS'] = 'true'
                    break

        if functions.verify('\nDo you want notifications on the discord server [Y/n]? > '):
            while 1:
                Config['DISCORD_WEBHOOK'] = str(input('Enter discord webhook > '))
                sleep(1)
                if functions.discordNotify('TEST', 'test notify', 'eb8e02') and functions.verify('Did you get the test message [Y/n]? > '):
                    Config['NOTIFY']['DISCORD'] = 'true'
                    break

        ConfigJson = dumps(Config)
        with open("config.json", "w") as config_file:
            config_file.write(ConfigJson)
            print("\nConfig save successful!")
            sleep(3)

        main.panel()