#!c:\users\wolfr\appdata\local\programs\python\python39\python.exe -m pip install --upgrade pip
from column_reader_thing.test1 import column_print
from web_client import close, recieve, change_username
from termcolor import cprint
from random import choice
from datetime import datetime
import database
from column_reader_thing.test1 import column_print
from os import listdir
from os.path import isfile, join

db = database.db("main.db","messages")
users_db = database.db("main.db","users")

db.setup("id","user","message","time")
users_db.setup("users","last message", "colour")

change_username("viewer")

colours = ["red","green","yellow","blue","magenta","cyan","white"]
broken_colours = ["grey"]
users = {}
first = True
past_messages = db.read()

while True:
    a = recieve() #listen for messages
    if a is not None: #if the message is a message
        user = a.get("user") #get the user that sent the message
        message = a.get("message") #and the message the user sent

        if first: #if this is the first message recieved
            first_user = user 
            last_message = users_db.select(user,1) #get the last message this user saw
            
            print(last_message)
            if last_message != []: #if they have logged on before
                last_message = int(last_message[0][1]) #get the id of the last message they saw
                for i in range(last_message,len(past_messages)): #loop through the the messages after
                    to_print = f"[PAST MESSAGE] [{past_messages[i][3]}]  {past_messages[i][1]}>{past_messages[i][2]}" #and display
                    print_colour = users_db.select(past_messages[i][1],1) #get the colour of the user that sent the message

                    if print_colour == []: #give the user a colour if they dont have one
                        print_colour = users_db.insert(past_messages[i][1], 0, choice(colours))
                        print_colour = users_db.select(past_messages[i][1],1)
                    print_colour = print_colour[0][2] #get the users colour
                    cprint(to_print, print_colour)  #print the past message with the correct colour
            first = False #disable first -> show this is not the first message
        if message.startswith("!"):
            message = message[1:].lower() # remove ! from message
            

            #---------------------------------------change text colour--------------------------------------------------

            if message.lower().startswith("change colour"): #it the message starts with "change colour" run this
                print(users_db.select(user,1)[0][2]) #get the current user
                colour = ""
                if len(message.split("change colour ")) != 1: #if they added args
                    print(message.split("change colour ")[1].split(" ")) 
                    if len(message.split("change colour ")[1]) != 0: #see how many
                        if len(message.split("change colour ")[1].split(" ")) == 1: #if it is 1
                            colour = message.split("change colour ")[1].split(" ")[0] #the new colour is that arg

                        if len(message.split("change colour ")[1].split(" ")) >= 2: #if they added 2 or more
                            colour = message.split("change colour ")[1].split(" ")[0] # the first one is the new colour
                            user = message.split("change colour ")[1].split(" ")[1] # the second one is the new user

                        if colour.lower() in colours or colour.lower() in ["rand", "random"]: #if they enetered a valid colour
                            if colour.lower() in ["rand","random"]: #if they enetered "rand" or "random"
                                colour = choice(colours) #set a random colour as the new colour
                            if users_db.select(user,1) == []: #if they have not saved before
                                last_message = len(db.read()) #read the current message
                                users_db.insert(user, last_message, colour) #add the user to the database

                            print(users_db.select(user,1)[0]) #read the user from the database
                            last_message = users_db.select(user,1)[0][1] #get there last message
                            users_db.remove(user,1) #remove there entry in the database
                            users_db.insert(user, last_message, colour) #insert there new entry with there new colour and old last message
                            continue #cycle to the last of the loop
            """
            
            if len(users_db.select("user",1)) != 0: #IM not sure what this does
                print("Ran")
                old_user = users[user]
                old_colour = old_user["colour"]
                while old_user["colour"] == old_colour:
                    old_user["colour"] = choice(colours)
                users[user] = old_user
                
            continue
            """

            if message.lower().startswith("list colours"): #if they enter "list colours"
                print("The avalable colours are:") 
                for colour in colours: #go through each colour
                    cprint(colour, colour) #print the colour name in the colour
                continue #cycle to the start of the loop
            
            if message.lower().startswith("help"): #if the message starts with help
                help_dir = "help_files/"
                help_files = [f for f in listdir(help_dir) if isfile(join(help_dir, f)) and f[-4:] == ".jrh"] #get all the .jrh files in the help folder
                print(help_files)
                help_commands = {
                    "help {optional_arg}":"Returns help on a specific command",
                    "list colours":"lists avalable printing colours",
                    "change colour {optional_colour} {optional_user}": "Changes text colour to a either a specified or random colour colour",
                    " ": "This is blank as a test"
                }
                if len(message.split("help ")) == 1:
                    
                    print("[INFO] The avalable commands are:")
                    for file in help_files:
                        print(file[:-4])
                    
                    continue

                file_to_find = message.split("help ")[1]
                file_to_find = f"{file_to_find}.jrh" 
                if file_to_find in help_files:
                    print(f"File {file_to_find}'s content is in green ")
                    
                    with open(f"{help_dir}/{file_to_find}","r") as f:
                        for x in f.readlines():
                            cprint(x.strip(), "green")
                    continue

            print(f"[INFO] Command {message} not found")
            continue


        if len(users_db.select(user,1)) == 0: # or users[user].get("colour", None) is None:
            
            users_db.insert(user, 0, choice(colours))
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
        past_messages = db.read()
        db.insert(len(past_messages),user,message,time)
        if message == "close":
            colour_to_insert = users_db.select(user,1)[0][2]
            users_db.remove(user,1)
            users_db.insert(user, len(past_messages), colour_to_insert)
            print(*users_db.read())
            if user == first_user:
                close()

        #print(users_db.select(user,1))
        #print(db.select(int(users_db.select(user,2)[0][0]),0))
        #column_print(db.select(int(db.select(user,2)[0][0]),0))
        to_print = f"[{time}]  {user}>{message}"
        cprint(to_print, users_db.select(user,1)[0][2]) 