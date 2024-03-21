# PACKAGES
try: # try import packages
    # EXTERNAL
    from time import sleep
    from json import load
    # OWN
    import functions
    from gui import GuiPanel
    from cli import CliPanel
except ImportError as error: # error handle
    print(f'\n\nModul not installed: {error}\n\n') # print error message + error
    sleep(3600) # wait 1h
    exit(1)

# MAIN
if __name__ == "__main__": # if file name is main then
    # CONFIG LOAD
    try: # try load config
        if functions.Verify('Want to load your config [Y/n]? > '): # if return value from Verify func from functions.py is true then
            with open("data/config.json", "r") as configFile: # opens config.json file and return a stream
                functions.Config = load(configFile) # load data from config.json and save into Config n-tice in main.py
                print("\nConfig load successful!\nConfig:")
            print(functions.Config) # print loaded config from functions.py
            input('\nPress enter for continue...')
    except: # error handle
        print('Config load failed!')
        sleep(3)

    # GUI VERSION
    if functions.Verify('\nWant to use gui [Y/n]? > '): # if return value from Verify func from functions.py is true then
        functions._Version = 'gui' # save value into Version var from functions.py
        GuiPanel() # call main function from gui.py
    # CLI VERSION
    else:
        # LINUX SUPPORT
        if functions.Verify('Using linux [Y/n]? > '): # if return value from Verify func from functions.py is true then
            functions._ClearCmd = 'clear' # save value into ClearCmd var from functions.py
        CliPanel() # call main function from cli.py