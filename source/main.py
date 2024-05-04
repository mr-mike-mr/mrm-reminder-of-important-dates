# PACKAGES
try: # try import packages
    # EXTERNAL
    from time import sleep
    import subprocess
    import sys
    # OWN
    import functions
    from cli import CliPanel
except ImportError as error: # error handle
    print(f'\n\nModul not installed: {error}\n\n') # print error message + error
    sleep(3600) # wait 1h
    exit(1)

# MAIN
if __name__ == "__main__": # if file name is main then
    # SERVER START
    if functions.Verify('Start SERVER [Y/n]? > '): # if return value from Verify func from functions.py is true then
        subprocess.Popen(['python', 'server.py']) # run server.py as a subprocess
        sys.exit() # exit from main.py

    # CLI START
    elif functions.Verify('Using linux [Y/n]? > '): # if return value from Verify func from functions.py is true then
        functions._ClearCmd = 'clear' # save value into ClearCmd var from functions.py
    CliPanel() # call main function from cli.py