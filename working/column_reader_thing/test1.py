import database
db = database.db("main.db","messages")

def column_print(messages):
    set_ammount = 3
    a = [ 
        [ [], 0 , "id"],
        [ [], 0 , "from"],
        [ [], 0 , "message"],
        [ [], 0 , "date/time"]
    ]

    for current_message in messages:
        for i in range(4):
            a[i][0].append(current_message[i])

    for i in range(len(a)):
        a[i][1] = max([len(j) for j in a[i][0]])
        
    for i in range(len(a)):
        print(a[i][2],end="")
        if int(a[i][1])-int(len(a[i][2])) >= 0:
            for j in range(int(a[i][1])-int(len(a[i][2]))):
                print(" ",end="")
            else:
                for i in range(set_ammount):
                    print(" ",end="")

    print("")
    p = 0
    for i in range(len(a)):
        p+=a[i][1]
    p += set_ammount*(len(a)-1)
    for i in range(p):
        print("-",end="")
    print("")
    for x in a:
        print(x)
    for j in range(len(a[0][0])):
        for i in range(len(a)):
            print(a[i][0][j],end="")
            b = [len(a[i][0][j]),0]
            b[1] = (int(a[i][1]) - b[0]) + set_ammount
            for k in range(b[1]-set_ammount):
                print(" ", end="")
            if i != len(a)-1:
                print(" | ", end= "")
        print("")
    print("")
if __name__ == "__main__":
    column_print(db.read())