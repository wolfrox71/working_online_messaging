#!/usr/bin/python
from web_client import send_message, get_message, change_username

change_username()
send_message("has arrived")
while True:
    message = get_message()
    if not not message:
        send_message(message)