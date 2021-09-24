#!/usr/bin/python
from typing import MutableSequence
import database
db = database.db("main.db","messages")
with open("messages.csv","w") as f:
    for x in db.read():
        f.write(f"{x[0]}, {x[1]}, {x[2]}, {x[3]}\n")