# TODO: make dokumentation
# TODO: make optimalization
try:
    from os import system
    from time import sleep
    from json import load

    import functions
    import config
    import databaseclient
    import server

except ImportError as error:
    print(f'\n\nModul not installed: {error}\n\n')
    sleep(60)
    exit(1)

def panel():
    while 1:
        system(config.CLEAR_CMD)
        print('### Reminder of Important Dates | PANEL ###')

        print('\n# OPTIONS:')
        print('1|Database Client')
        print('2|Config')
        print('3|Server')
        print('4|Exit')

        option = functions.numInput('\nSelect option > ')

        if option == 1:
            databaseclient.Main()
        elif option == 2:
            config.Main()
        elif option == 3:
            server.Main()
        elif option == 4:
            if functions.verify('Want to exit [Y/n]? > '):
                exit(1)
        else:
            print('Wrong option!')
            sleep(2)

if __name__ == "__main__":
    if functions.verify('\n\nUsing linux [Y/n]? > '):
        config.CLEAR_CMD = 'clear'

    if functions.verify('Want to load your config [Y/n]? > '):
        with open("config.json", "r") as config_file:
            config.Config = load(config_file)
            print("\nConfig load successful!\nConfig:")
        print(config.Config)
        sleep(3)

    panel()