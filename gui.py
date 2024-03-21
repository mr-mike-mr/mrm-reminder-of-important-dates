# PACKAGES
try: # try import packages
    # EXTERNAL
    from time import sleep
    from tkinter import Frame, Label, Entry, Button, Tk, IntVar, Checkbutton, messagebox, Canvas, Scrollbar
    import threading
    # OWN
    #from functions import Config, Server, NumInput, AddDate, RemoveData, DatabaseConnect, DatabaseDisconnect, SaveConfig, EmailNotify, SmsNotify, DiscordNotify
    import functions
except ImportError as error: # error handle
    print(f'\n\nModul not installed: {error}\n\n') # print error message + error
    sleep(3600) # sleep 1h
    exit(1)

# GUI CONFIG FUNC
def gui_config(root): # root = screen widget
    # SAVE BUTTON FUNC
    def save_button():
        if messagebox.askquestion("Config save", 'Are you sure?') == 'yes' and functions.NumInput(value = refresh_time_entry.get()): # if askquestion from tkinter is yes and return value from NumInput() then
            functions.Config['REFRESH_TIME'] = (int(refresh_time_entry.get()) * 3600) # call get func from tkinter for get value from smtp_server_entry, turns into hours and save into Config['REFRESH_TIME'] in functions.py
            functions.Config['SMTP_SERVER'] = smtp_server_entry.get() # call get func from tkinter for get value from smtp_server_entry and save into Config['SMTP_SERVER'] in functions.py
            functions.Config['SMTP_PORT'] = smtp_port_entry.get() # call get func from tkinter for get value from smtp_port_entry and save into Config['SMTP_PORT'] in functions.py
            functions.Config['SMTP_EMAIL'] = smtp_email_entry.get() # call get func from tkinter for get value from smtp_email_entry and save into Config['SMTP_EMAIL'] in functions.py
            functions.Config['SMTP_PASSWORD'] = smtp_password_entry.get() # call get func from tkinter for get value from smtp_password_entry and save into Config['SMTP_PASSWORD'] in functions.py
            functions.Config['SMTP_CLIENT_EMAIL'] = smtp_client_email_entry.get() # call get func from tkinter for get value from smtp_client_email_entry and save into Config['SMTP_CLIENT_EMAIL'] in functions.py
            functions.Config['SMS_TOKEN'] = sms_token_entry.get() # call get func from tkinter for get value from sms_token_entry and save into Config['SMS_TOKEN'] in functions.py
            functions.Config['SMS_SID'] = sms_sid_entry.get() # call get func from tkinter for get value from sms_sid_entry and save into Config['SMS_SID'] in functions.py
            functions.Config['SMS_TWILIO_PHONE'] = sms_twilio_phone_entry.get() # call get func from tkinter for get value from sms_twilio_phone_entry and save into Config['SMS_TWILIO_PHONE'] in functions.py
            functions.Config['SMS_CLIENT_PHONE'] = sms_client_phone_entry.get() # call get func from tkinter for get value from sms_client_phone_entry and save into Config['SMS_CLIENT_PHONE'] in functions.py
            functions.Config['DISCORD_WEBHOOK'] = discord_entry.get() # call get func from tkinter for get value from discord_entry and save into Config['DISCORD_WEBHOOK'] in functions.py
            functions.Config['NOTIFY']['EMAIL'] = True if notiy_smtp.get() else False # call get func from tkinter for get value from notiy_smtp and if is 1 then save True else False and save into Config['NOTIFY']['EMAIL'] in functions.py
            functions.Config['NOTIFY']['SMS'] = True if notiy_sms.get() else False # call get func from tkinter for get value from notiy_sms and if is 1 then save True else False and save into Config['NOTIFY']['SMS'] in functions.py
            functions.Config['NOTIFY']['DISCORD'] = True if notiy_discord.get() else False # call get func from tkinter for get value from notiy_discord and if is 1 then save True else False and save into Config['NOTIFY']['DISCORD'] in functions.py
            functions.SaveConfig() # call SaveConfig func from functions.py for save config
            reset_button() # call reset_button func for reset entrys

    # RESET BUTTON FUNC
    def reset_button():
        if messagebox.askquestion("Reset config entrys", 'Are you sure?') == 'yes': # if askquestion from tkinter is yes then
            refresh_time_entry.delete(0, 'end') # call delete func from functions.py for delete text from refresh_time_entry
            smtp_server_entry.delete(0, 'end') # call delete func from functions.py for delete text from smtp_server_entry
            smtp_port_entry.delete(0, 'end') # call delete func from functions.py for delete text from smtp_port_entry
            smtp_email_entry.delete(0, 'end') # call delete func from functions.py for delete text from smtp_email_entry
            smtp_password_entry.delete(0, 'end') # call delete func from functions.py for delete text from smtp_password_entry
            smtp_client_email_entry.delete(0, 'end') # call delete func from functions.py for delete text from smtp_client_email_entry
            sms_token_entry.delete(0, 'end') # call delete func from functions.py for delete text from sms_token_entry
            sms_sid_entry.delete(0, 'end') # call delete func from functions.py for delete text from sms_sid_entry
            sms_twilio_phone_entry.delete(0, 'end') # call delete func from functions.py for delete text from sms_twilio_phone_entry
            sms_client_phone_entry.delete(0, 'end') # call delete func from functions.py for delete text from sms_client_phone_entry
            discord_entry.delete(0, 'end') # call delete func from functions.py for delete text from discord_entry
            notiy_smtp.set(0) # call set func from tkinter fro set notiy_smtp checkbox to 0
            notiy_sms.set(0) # call set func from tkinter fro set notiy_sms checkbox to 0
            notiy_discord.set(0) # call set func from tkinter fro set notiy_discord checkbox to 0

    # SMTP TEST BUTTON FUNC
    def smtp_test_button():
        if messagebox.askquestion("Smtp test", 'Are you sure?') == 'yes': # if askquestion from tkinter is yes then
            functions.Config['SMTP_SERVER'] = smtp_server_entry.get() # call get func from tkinter for get value from smtp_server_entry and save into Config['SMTP_SERVER'] in functions.py
            functions.Config['SMTP_PORT'] = smtp_port_entry.get() # call get func from tkinter for get value from smtp_port_entry and save into Config['SMTP_PORT'] in functions.py
            functions.Config['SMTP_EMAIL'] = smtp_email_entry.get() # call get func from tkinter for get value from smtp_email_entry and save into Config['SMTP_EMAIL'] in functions.py
            functions.Config['SMTP_PASSWORD'] = smtp_password_entry.get() # call get func from tkinter for get value from smtp_password_entry and save into Config['SMTP_PASSWORD'] in functions.py
            functions.Config['SMTP_CLIENT_EMAIL'] = smtp_client_email_entry.get() # call get func from tkinter for get value from smtp_client_email_entry and save into Config['SMTP_CLIENT_EMAIL'] in functions.py
            functions.EmailNotify('TEST', 'test notify') # call EmailNotify func from functions.py for test notify
            messagebox.showinfo("Smtp", "Successful!") # show tkinter info messagebox

    # SMS TEST BUTTON FUNC
    def sms_test_button():
        if messagebox.askquestion("Sms test", 'Are you sure?') == 'yes': # if askquestion from tkinter is yes then
            functions.Config['SMS_TOKEN'] = sms_token_entry.get() # call get func from tkinter for get value from sms_token_entry and save into Config['SMS_TOKEN'] in functions.py
            functions.Config['SMS_SID'] = sms_sid_entry.get() # call get func from tkinter for get value from sms_sid_entry and save into Config['SMS_SID'] in functions.py
            functions.Config['SMS_TWILIO_PHONE'] = sms_twilio_phone_entry.get() # call get func from tkinter for get value from sms_twilio_phone_entry and save into Config['SMS_TWILIO_PHONE'] in functions.py
            functions.Config['SMS_CLIENT_PHONE'] = sms_client_phone_entry.get() # call get func from tkinter for get value from sms_client_phone_entry and save into Config['SMS_CLIENT_PHONE'] in functions.py
            functions.SmsNotify('test notify') # call SmsNotify func from functions.py for test notify
            messagebox.showinfo("Twilio", "Successful!") # show tkinter info messagebox

    # DISCORD TEST BUTTON FUNC
    def discord_test_button():
        if messagebox.askquestion("Discord test", 'Are you sure?') == 'yes': # if askquestion from tkinter is yes then
            functions.Config['DISCORD_WEBHOOK'] = discord_entry.get() # call get func from tkinter for get value from discord_entry and save into Config['DISCORD_WEBHOOK'] in functions.py
            functions.DiscordNotify('TEST', 'test notify', 'eb8e02') # call DiscordNotify func from functions.py for test notify
            messagebox.showinfo("Discord", "Successful!") # show tkinter info messagebox

    # FRAME
    config_frame = Frame(root, height=300, width=300, highlightbackground="black", highlightthickness=2) # call Frame func from tkinter for construct a frame widget with the parent root

    # TITLE
    Label(config_frame, text='CONFIG', pady=0, padx=0, font=6).grid(row=0, columnspan=2, sticky='we') # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget

    # SMTP SERVER CONFIG
    Label(config_frame, text='Enter smtp server', pady=0, padx=0, font=6).grid(row=1, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    smtp_server_entry = Entry(config_frame, width=100) # call Entry func from tkinter for construct an entry widget with the parent config_frame
    smtp_server_entry.grid(row=1, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid
    # SMTP PORT CONFIG
    Label(config_frame, text='Enter smtp port', pady=0, padx=0, font=6).grid(row=2, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    smtp_port_entry = Entry(config_frame, width=100) # call Entry func from tkinter for construct an entry widget with the parent config_frame
    smtp_port_entry.grid(row=2, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid
    # SMTP EMAIL CONFIG
    Label(config_frame, text='Enter smtp email', pady=0, padx=0, font=6).grid(row=3, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    smtp_email_entry = Entry(config_frame, width=100) # call Entry func from tkinter for construct an entry widget with the parent config_frame
    smtp_email_entry.grid(row=3, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid
    # SMTP PASSWORD CONFIG
    Label(config_frame, text='Enter smtp password', pady=0, padx=0, font=6).grid(row=4, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    smtp_password_entry = Entry(config_frame, width=100, show="*") # call Entry func from tkinter for construct an entry widget with the parent config_frame
    smtp_password_entry.grid(row=4, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid
    # SMTP CLIENT EMAIL CONFIG
    Label(config_frame, text='Enter your email', pady=0, padx=0, font=6).grid(row=5, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    smtp_client_email_entry = Entry(config_frame, width=100) # call Entry func from tkinter for construct an entry widget with the parent config_frame
    smtp_client_email_entry.grid(row=5, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid
    # SMTP TEST
    Button(config_frame, width=25, text='SMTP test', command=smtp_test_button).grid(row=6, column=0, columnspan=2) # smtp test | call Button func from tkinter for construct stop server button widget with the parent config_frame | call grid func from functions.py for position a widget in the parent widget in a grid

    # SMS TOKEN CONFIG
    Label(config_frame, text='Enter twilio token', pady=0, padx=0, font=6).grid(row=7, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    sms_token_entry = Entry(config_frame, width=100, show="*") # call Entry func from tkinter for construct an entry widget with the parent config_frame
    sms_token_entry.grid(row=7, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid
    # SMS SID CONFIG
    Label(config_frame, text='Enter twilio sid', pady=0, padx=0, font=6).grid(row=8, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    sms_sid_entry = Entry(config_frame, width=100, show="*") # call Entry func from tkinter for construct an entry widget with the parent config_frame
    sms_sid_entry.grid(row=8, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid
    # SMS PHONE NUMBER CONFIG
    Label(config_frame, text='Enter twilio phone number', pady=0, padx=0, font=6).grid(row=9, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    sms_twilio_phone_entry = Entry(config_frame, width=100) # call Entry func from tkinter for construct an entry widget with the parent config_frame
    sms_twilio_phone_entry.grid(row=9, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid
    # SMS CLIENT PHONE NUMBER CONFIG
    Label(config_frame, text='Enter yout phone number', pady=0, padx=0, font=6).grid(row=10, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    sms_client_phone_entry = Entry(config_frame, width=100) # call Entry func from tkinter for construct an entry widget with the parent config_frame
    sms_client_phone_entry.grid(row=10, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid
    # SMS TEST
    Button(config_frame, width=25, text='Twilio test', command=sms_test_button).grid(row=11, column=0, columnspan=2) # sms test | call Button func from tkinter for construct stop server button widget with the parent config_frame | call grid func from functions.py for position a widget in the parent widget in a grid

    # DISCORD WEBHOOK CONGFIG
    Label(config_frame, text='Enter discord webhook', pady=0, padx=0, font=6).grid(row=12, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    discord_entry = Entry(config_frame, width=100, show="*") # call Entry func from tkinter for construct an entry widget with the parent config_frame
    discord_entry.grid(row=12, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid
    # DISCORD TEST
    Button(config_frame, width=25, text='Discord test', command=discord_test_button).grid(row=13, column=0, columnspan=2) # discord test | call Button func from tkinter for construct stop server button widget with the parent config_frame | call grid func from functions.py for position a widget in the parent widget in a grid

    Label(config_frame, text='Enter server refresh time [hod.]', pady=0, padx=0, font=6, justify="left").grid(row=14, sticky="we") # call Label func from tkinter for construct a label widget with the parent config_frame | call pack func from tkinter for pack a widget in the parent widget
    refresh_time_entry = Entry(config_frame, width=100) # call Entry func from tkinter for construct an entry widget with the parent config_frame
    refresh_time_entry.grid(row=14, column=1, sticky="we") # call grid func from functions.py for position a widget in the parent widget in a grid

    # NOTIFY CHECKBUTTONS
    notiy_smtp = IntVar() # call IntVar func from tkinter for construct an integer variable
    notiy_sms = IntVar() # call IntVar func from tkinter for construct an integer variable
    notiy_discord = IntVar() # call IntVar func from tkinter for construct an integer variable
    notiy_smtp_checkbutton = Checkbutton(config_frame, text="SMTP notify", variable=notiy_smtp) # smtp notify | call Checkbutton func from tkinter for construct a checkbutton widget with the parent config_frame
    notiy_smtp_checkbutton.grid(row=15, column=0, columnspan=2, sticky='we') # call grid func from functions.py for position a widget in the parent widget in a grid
    notiy_sms_checkbutton = Checkbutton(config_frame, text="SMS notify", variable=notiy_sms) # sms notify | call Checkbutton func from tkinter for construct a checkbutton widget with the parent config_frame
    notiy_sms_checkbutton.grid(row=16, column=0, columnspan=2, sticky='we') # call grid func from functions.py for position a widget in the parent widget in a grid
    notiy_discord_checkbutton = Checkbutton(config_frame, text="Discord notify", variable=notiy_discord) # discord notify | call Checkbutton func from tkinter for construct a checkbutton widget with the parent config_frame
    notiy_discord_checkbutton.grid(row=17, column=0, columnspan=2, sticky='we') # call grid func from functions.py for position a widget in the parent widget in a grid

    # CONTROL BUTTONS
    Button(config_frame, width=25, text='Save', command=save_button).grid(row=18, column=0, columnspan=2, sticky="we") # save config | call Button func from tkinter for construct stop server button widget with the parent config_frame | call grid func from functions.py for position a widget in the parent widget in a grid
    Button(config_frame, width=25, text='Resetting entries', command=reset_button).grid(row=19, column=0, columnspan=2, sticky="we") # reset entriess | call Button func from tkinter for construct stop server button widget with the parent config_frame | call grid func from functions.py for position a widget in the parent widget in a grid

    # FRAME PLACE
    config_frame.grid(row=1, column=0, columnspan=2, sticky='wens') # call grid func from tkinter for position a widget in the parent widget in a grid
    # ROW AND COLUMN CONFIG
    config_frame.grid_rowconfigure(0, minsize=0, weight=1) # call grid_rowconfigure func from tkinter for configure row index of a grid
    config_frame.grid_columnconfigure(0, minsize=0, weight=1) # call grid_columnconfigure func from tkinter for configure column index of a grid

# GUI DATABASE CLIENT FUNC
def gui_databaseclient(root): # root = screen widget
    # DATE INPUT FUNC
    def _date_input(value): # value = value for check
        if value.count(".") == 2: # if it is in value 2 times . then
            value_array = value.split(".") # splitting the string by . into an array
            for i in range(2): # pass the array
                if functions.NumInput(value=str(value_array[i])): # call NumInput func from functions.py for check if the value is a number
                    value_array[i] = int(value_array[i]) # cast to value number and save
            if value_array[0] >= 0 and value_array[0] <= 31 and value_array[1] >= 0 and value_array[1] <= 12: # if day more or equal to 0 and less or equal to 31 and month more or equal to 0 and less or equal to 12 then
                return True
        messagebox.showwarning('Date format', 'Incorrect date format [dd.mm.yyyy]!') # show tkinter warning messagebox
        return False

    # ADD BUTTON FUNC
    def add_button():
        if messagebox.askquestion("Add date", 'Are you sure?') == 'yes': # if askquestion from tkinter is yes then
            if _date_input(date_entry.get()) and _date_input(warn_date_entry.get()): # and if return values from _date_input is true then
                functions.AddDate(text_entry.get(), date_entry.get(), warn_date_entry.get()) # call AddDate func from functions.py for add new date/row into database
                messagebox.showinfo("Add date", "Successful!") # show tkinter info messagebox
                text_entry.delete(0, 'end') # call delete func from functions.py for delete text from text_entry
                date_entry.delete(0, 'end') # call delete func from functions.py for delete text from date_entry
                warn_date_entry.delete(0, 'end') # call delete func from functions.py for delete text from warn_date_entry
                consol_show() # call refresh_button func for refresh console

    # REMOVE BUTTON FUNC
    def remove_button():
        if messagebox.askquestion("Remove date", 'Are you sure?') == 'yes' and functions.NumInput(value=id_entry.get()): # if askquestion from tkinter is yes and return value from NumInput() then
            functions.RemoveData(int(id_entry.get())) # call RemoveData func from functions.py for remove date/row into database
            messagebox.showinfo("Remove date", "Successful!") # show tkinter info messagebox
            id_entry.delete(0, 'end') # call delete func from functions.py for delete text from id_entry
            consol_show() # call refresh_button func for refresh console

    # CONSOLE SHOW FUNC
    def consol_show():
        # MAIN FRAME
        database_show_frame = Frame(databaseclient_frame, highlightbackground="black", highlightthickness=2) # call Frame func from tkinter for construct a frame widget with the parent database_show_frame
        database_show_frame.grid(row=0, column=0, columnspan=2, sticky='wens') # call grid func from tkinter for position a widget in the parent widget in a grid

        # CANVAS
        database_show_canvas = Canvas(database_show_frame) # call Canvas func from tkinter for construct a canvas widget with the parent database_show_frame
        database_show_scrollbar = Scrollbar(database_show_frame, orient="vertical", command=database_show_canvas.yview) # call Scrollbar func from tkinter for construct a scrollbar widget with the parent database_show_frame
        database_show_canvas.configure(yscrollcommand=database_show_scrollbar.set) # call configure func from tkinter for configure scrollbar widget

        # SCROLL CONTENT FRAME
        database_show_content_frame = Frame(database_show_canvas) # call Frame func from tkinter for construct a frame widget with the parent database_show_canvas
        database_show_content_frame.bind("<Configure>", lambda e: database_show_canvas.configure(scrollregion=database_show_canvas.bbox("all"))) # call bind func from tkinter for bind to this widget at event sequence for show all

        # ROW AND COLUMN CONFIG
        root.columnconfigure(0, weight=1) # call grid_columnconfigure func from tkinter for configure column index of a grid
        database_show_frame.columnconfigure(0, weight=1) # call grid_columnconfigure func from tkinter for configure column index of a grid
        root.rowconfigure(0, weight=1) # call grid_rowconfigure func from tkinter for configure row index of a grid
        database_show_frame.rowconfigure(0, weight=1) # call grid_rowconfigure func from tkinter for configure row index of a grid

        # FRAME PLACE
        database_show_canvas.create_window((0, 0), window=database_show_content_frame, anchor="nw") # call create_window func from tkinter for create window with coordinates x1, y1
        database_show_canvas.grid(row=0, column=0, sticky="nsew") # call grid func from tkinter for position a widget in the parent widget in a grid
        database_show_scrollbar.grid(row=0, column=1, sticky="ns") # call grid func from tkinter for position a widget in the parent widget in a grid

        # MOUSE WHEEL SCROLL FUNC
        def _on_mousewheel(event): # event = get mouse wheel data
           database_show_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") # calculates the number by how much to move and call yview_scroll func from tkinter
        database_show_canvas.bind_all("<MouseWheel>", _on_mousewheel) # call bind_all func from tkinter for bind to all widget at event sequence for get mouse wheel event

        # SHOW DATES
        db = functions.DatabaseConnect() # call DatabaseConnect func from functions.py for connect/open database and save database objects
        for row in db[1].execute("SELECT * FROM Dates"): # goes through all rows in the database
            Label(database_show_content_frame, text=f'{row[0]} | {row[1]} | {row[2]} | {row[3]}', pady=0, padx=0, font=6).pack(fill='none') # 'row[id] | row[text] | row[date] | row[warn_date]' | call Label func from tkinter for construct a label widget with the parent database_show_content_frame | call pack func from tkinter for pack a widget in the parent widget
        functions.DatabaseDisconnect(db[0]) # call DatabaseDisconnect func from functions.py for disconnect/close database

    # FRAMES
    databaseclient_frame = Frame(root, height=500, width=600, highlightbackground="black", highlightthickness=2) # call Frame func from tkinter for construct a frame widget with the parent root
    consol_show() # call refresh_button func

    # REFRESH
    Button(databaseclient_frame, width=25, text='Refresh', command=consol_show).grid(row=1, column=0, columnspan=2, sticky="we") # refresh database rows | call Button func from tkinter for construct stop server button widget with the parent databaseclient_frame | call grid func from functions.py for position a widget in the parent widget in a grid

    # TEXT ADD LABEL
    Label(databaseclient_frame, text='Text', pady=0, padx=0, font=6, justify="left").grid(row=2, sticky="we") # call Label func from tkinter for construct a label widget with the parent databaseclient_frame | call pack func from tkinter for pack a widget in the parent widget
    text_entry = Entry(databaseclient_frame, width=50) # call Entry func from tkinter for construct an entry widget with the parent databaseclient_frame
    text_entry.grid(row=2, column=1) # call grid func from tkinter for position a widget in the parent widget in a grid
    # DATE ADD LABEL
    Label(databaseclient_frame, text='Date', pady=0, padx=0, font=6, justify="left").grid(row=3, sticky="we") # call Label func from tkinter for construct a label widget with the parent databaseclient_frame | call pack func from tkinter for pack a widget in the parent widget
    date_entry = Entry(databaseclient_frame, width=50) # call Entry func from tkinter for construct an entry widget with the parent databaseclient_frame
    date_entry.grid(row=3, column=1) # call grid func from tkinter for position a widget in the parent widget in a grid
    # WARN DATE ADD LABEL
    Label(databaseclient_frame, text='Warn date', pady=0, padx=0, font=6, justify="left").grid(row=4, sticky="we") # call Label func from tkinter for construct a label widget with the parent databaseclient_frame | call pack func from tkinter for pack a widget in the parent widget
    warn_date_entry = Entry(databaseclient_frame, width=50) # call Entry func from tkinter for construct an entry widget with the parent databaseclient_frame
    warn_date_entry.grid(row=4, column=1) # call grid func from tkinter for position a widget in the parent widget in a grid
    # ADD BUTTON
    Button(databaseclient_frame, width=25, text='Add', command=add_button).grid(row=5, column=0, columnspan=2, sticky="we") # add row into database | call Button func from tkinter for construct stop server button widget with the parent databaseclient_frame | call grid func from functions.py for position a widget in the parent widget in a grid

    # ID REMOVE LABEL
    Label(databaseclient_frame, text='Id', pady=0, padx=0, font=6, justify="left").grid(row=6, sticky="we") # call Label func from tkinter for construct a label widget with the parent databaseclient_frame | call pack func from tkinter for pack a widget in the parent widget
    id_entry = Entry(databaseclient_frame, width=50) # call Entry func from tkinter for construct an entry widget with the parent databaseclient_frame
    id_entry.grid(row=6, column=1) # call grid func from tkinter for position a widget in the parent widget in a grid
    # REMOVE BUTTON
    Button(databaseclient_frame, width=25, text='Remove', command=remove_button).grid(row=7, column=0, columnspan=2, sticky="we") # remove row from database | call Button func from tkinter for construct stop server button widget with the parent databaseclient_frame | call grid func from functions.py for position a widget in the parent widget in a grid

    # FRAME PLACE
    databaseclient_frame.grid(row=0, column=0, sticky='wens') # call grid func from tkinter for position a widget in the parent widget in a grid
    # ROW AND COLUMN CONFIG
    databaseclient_frame.grid_rowconfigure(0, minsize=0, weight=1) # call grid_rowconfigure func from tkinter for configure row index of a grid
    databaseclient_frame.grid_columnconfigure(0, minsize=0, weight=1) # call grid_columnconfigure func from tkinter for configure column index of a grid

# GUI SERVER
def gui_server(root): # root = screen widget
    # START BUTTON FUNC
    def start_button():
        functions._ServerStatus = True
        consol_show_thread = threading.Thread(target=consol_show) # call thread func from threading for make thread constructor targeted on consol_show func
        consol_show_thread.start() # call start func from threading for start the thread's activity from _ConsolShowThread thread constructor
        messagebox.showinfo("Start server", "Start successful!") # show tkinter info messagebox

    # CONSOL SHOW FUNC
    def consol_show():
        # MAIN FRAME
        server_show_frame = Frame(server_frame, highlightbackground="black", highlightthickness=2) # call Frame func from tkinter for construct a frame widget with the parent server_frame
        server_show_frame.grid(row=0, column=0, columnspan=2, sticky='wens') # call grid func from tkinter for position a widget in the parent widget in a grid

        # CANVAS
        server_show_canvas = Canvas(server_show_frame) # call Canvas func from tkinter for construct a canvas widget with the parent server_show_frame
        server_show_scrollbar = Scrollbar(server_show_frame, orient="vertical", command=server_show_canvas.yview) # call Scrollbar func from tkinter for construct a scrollbar widget with the parent server_show_frame
        server_show_canvas.configure(yscrollcommand=server_show_scrollbar.set) # call configure func from tkinter for configure scrollbar widget

        # SCROLL CONTENT FRAME
        server_show_content_frame = Frame(server_show_canvas) # call Frame func from tkinter for construct a frame widget with the parent server_show_canvas
        server_show_content_frame.bind("<Configure>", lambda e: server_show_canvas.configure(scrollregion=server_show_canvas.bbox("all"))) # call bind func from tkinter for bind to this widget at event sequence for show all

        # ROW AND COLUMN CONFIG
        root.columnconfigure(0, weight=1) # call grid_columnconfigure func from tkinter for configure column index of a grid
        server_show_frame.columnconfigure(0, weight=1) # call grid_columnconfigure func from tkinter for configure column index of a grid
        root.rowconfigure(0, weight=1) # call grid_rowconfigure func from tkinter for configure row index of a grid
        server_show_frame.rowconfigure(0, weight=1) # call grid_rowconfigure func from tkinter for configure row index of a grid

        # FRAME PLACE
        server_show_canvas.create_window((0, 0), window=server_show_content_frame, anchor="nw") # call create_window func from tkinter for create window with coordinates x1, y1
        server_show_canvas.grid(row=0, column=0, sticky="nsew") # call grid func from tkinter for position a widget in the parent widget in a grid
        server_show_scrollbar.grid(row=0, column=1, sticky="ns") # call grid func from tkinter for position a widget in the parent widget in a grid

        # MOUSE WHEEL SCROLL FUNC
        def _on_mousewheel(event): # event = get mouse wheel data
           server_show_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") # calculates the number by how much to move and call yview_scroll func from tkinter
        server_show_canvas.bind_all("<MouseWheel>", _on_mousewheel) # call bind_all func from tkinter for bind to all widget at event sequence for get mouse wheel event

        functions.Server(server_show_content_frame) # call Server func from functions.py for run server

    # FRAMES
    server_frame = Frame(root, height=300, width=300, highlightbackground="black", highlightthickness=2) # call Frame func from tkinter for construct a frame widget with the parent root
    consol_show() # call consol_show func for show server frame

    # BUTTONS
    Button(server_frame, width=25, text='Start', command=start_button).grid(row=1, column=0, columnspan=2, sticky='wens') # start server | call Button func from tkinter for construct start server button widget with the parent server_frame | call grid func from functions.py for position a widget in the parent widget in a grid

    # FRAME PLACE
    server_frame.grid(row=0, column=1, sticky='wens') # call grid func from tkinter for position a widget in the parent widget in a grid
    # ROW AND COLUMN CONFIG
    server_frame.grid_rowconfigure(0, minsize=0, weight=1) # call grid_rowconfigure func from tkinter for configure row index of a grid
    server_frame.grid_columnconfigure(0, minsize=0, weight=1) # call grid_columnconfigure func from tkinter for configure column index of a grid

# GUI PANEL FUNC
def GuiPanel():
    # SCREEN WIDGET
    root = Tk() # call Tk func from tkinter for return a new top level widget on screen
    root.iconbitmap("data/favicon.ico") # call iconbitmap func from tkinter for set bitmap for the iconified widget
    root.title('Reminder of Important Dates') # call title func from tkinter for set the title of this widget
    root.minsize(930, 800) # call minsize func from tkinter for Set min width and height for this widget

    # FRAMES
    gui_databaseclient(root) # call gui_databaseclient func for make databaseclient frame
    gui_config(root) # call gui_config func for make config frame
    gui_server(root) # call gui_server func for make server frame

    # ROW AND COLUMN CONFIG
    root.grid_rowconfigure(0, minsize=300, weight=1) # call grid_rowconfigure func from tkinter for configure row index of a grid
    root.grid_columnconfigure(0, minsize=300, weight=1) # call grid_columnconfigure func from tkinter for configure column index of a grid
    root.grid_columnconfigure(1, minsize=300, weight=1) # call grid_columnconfigure func from tkinter for configure column index of a grid

    # START
    root.mainloop() # call the mainloop of Tk