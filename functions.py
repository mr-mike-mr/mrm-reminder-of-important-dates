# TODO: make dokumentation
# TODO: optimalizate
try:
    from time import sleep
    from sqlite3 import connect, Error
    from discord_webhook import DiscordWebhook, DiscordEmbed
    from twilio.rest import Client
    import smtplib

    import config

except ImportError as error:
    print(f'\n\nModul not installed: {error}\n\n')
    sleep(60)
    exit(1)

def error(text):
    print(f'\n\n{text}\n\nPlease contact support: https://discord.com/invite/SK8Z3uV72k \n\n')
    sleep(60)
    exit(1)

def verify(text):
    while 1:
        value = str(input(text))
        if value == 'Y' or value == 'y':
            return True
        if value == 'N' or value == 'n':
            return False
        else:
            print('The answer must be \'Y/n\'!\n')
            sleep(2)

def numInput(text):
    while 1:
        try:
            value = int(input(text))
            return value
        except:
            print('Input must be number!\n')

def databaseConnect():
    try:
        db_connect = connect('database.db')
    except Error as error:
        error(f'Database open failed: {error}')

    db_cursor = db_connect.cursor()
    return [db_connect, db_cursor]

def databaseDisconnect(db_connect):
    try:
        db_connect.close()
    except Error as error:
        error(f'Database close failed: {error}')

def emailNotify(title, text):
    try:
        with smtplib.SMTP(config.Config['SMTP_SERVER'], config.Config['SMTP_PORT']) as smtp:
            smtp.starttls()
            smtp.login(config.Config['SMTP_EMAIL'], config.Config['SMTP_PASSWORD'])
            smtp.sendmail(config.Config['SMTP_EMAIL'], config.Config['CLIENT_EMAIL'], f'Subject: Reminder of Importrant Dates - {title}\n\n{text}')
        return True
    except:
        print('Incorrect smtp service values!\n')
        sleep(3)
        return False

def smsNotify(message):
    try:
        client = Client(config.Config['SMS_SID'], config.Config['SMS_TOKEN'])
        message = client.messages.create(
            from_ = config.Config['SMS_TWILIO_PHONE'],
            body = message,
            to = config.Config['SMS_CLIENT_PHONE']
        )
        return True
    except:
        print('Incorrect twilio service values!\n')
        sleep(3)
        return False

def discordNotify(title, message, color):
    try:
        webhook = DiscordWebhook(url=config.Config['DISCORD_WEBHOOK'], rate_limit_retry=True)
        embed = DiscordEmbed(title=title, description=message, color=color)
        embed.set_author(name='Reminder-of-Important-Dates', url='https://github.com/mr-mike-mr')
        embed.set_footer(text='Created By mr.mike3319')
        webhook.add_embed(embed)
        webhook.execute()
        return True
    except:
        print('Incorrect discord webhook!\n')
        sleep(3)
        return False