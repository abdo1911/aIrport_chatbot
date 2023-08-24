from tkinter import *
from tkinter import messagebox
import mysql.connector
from wit import Wit
from flask import Flask, render_template, request
from fuzzywuzzy import fuzz,process

access_token = "KOX4VWOFKRFLCJWB5THLKFH5PHLCLJOT"
client = Wit(access_token=access_token)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="chatbot"
)

mycursor = db.cursor()

def dist(q):
    abdo = db.cursor()
    abdo.execute("select question from main")
    result = abdo.fetchall()
    #for x in result:
        #print(x)

    max=-9999
    stringa = q
    z=""

    for x in result:
        if (fuzz.ratio(stringa, x) > 75):
            print("This is similar to ", x)
            m = fuzz.ratio(stringa, x)
            if m > max:
                max=m
                z=stringa
            print(m)
    print("this is the max : ",max)
    print("this is sentence : ",z)
    txt.insert(END, "\n" + "bot : do you mean : " + z)

def mainscreen():
    global screen
    global usermail
    global password

    screen = Tk()
    screen.geometry("1280x720+150+70")
    screen.configure(bg='#d7dae2')
    screen.title("Login Page")

    lbltitle = Label(text="Login Page", font=("arial", 50, "bold"), fg="black", bg="#d7dae2")
    lbltitle.pack(pady=50)

    bordercolor = Frame(screen, bg="black", width=800, height=400)
    bordercolor.pack()
    mainframe = Frame(bordercolor, bg="#d7dae2", width=800, height=400)
    mainframe.pack(padx=20, pady=20)

    usermail = StringVar()
    password = StringVar()

    usermaillabel = Label(mainframe, text="usermail", font=("arial", 30, "bold"), bg="#d7dae2")
    usermaillabel.place(x=100, y=50)
    entryusername = Entry(mainframe, textvariable=usermail, width=12, bd=2, font=("arial", 30))
    entryusername.place(x=400, y=50)

    userpasslabel = Label(mainframe, text="password", font=("arial", 30, "bold"), bg="#d7dae2")
    userpasslabel.place(x=100, y=150)
    entrypassword = Entry(mainframe, textvariable=password, width=12, bd=2, font=("arial", 30), show="*")
    entrypassword.place(x=400, y=150)

    button1 = Button(mainframe, text="Login", height="2", width=23, bg="#ed3833", fg="white", bd=0, command=login)
    button1.place(x=100, y=250)
    button2 = Button(mainframe, text="Signup", height="2", width=23, bg="#ed3833", fg="white", bd=0, command=signup)
    button2.place(x=300, y=250)
    button3 = Button(mainframe, text="Exit", height="2", width=23, bg="#ed3833", fg="white", bd=0,
                     command=screen.destroy)
    button3.place(x=500, y=250)

    screen.mainloop()

def login():
    global user_id
    user = usermail.get()
    code = password.get()
    mycursor = db.cursor(buffered=True)
    sql = "select count(*) from user where email = %s and password = %s"
    mycursor.execute(sql, (user, code))
    result = mycursor.fetchone()[0]
    mycursorr = db.cursor()
    mycursorr.execute("select user_id from user WHERE email =" + "'" + user + "'")
    user_id = mycursorr.fetchone()[0]
    print(user_id)
    # print(result)
    if result == 1:
        screen.destroy()
        global e
        global txt
        root = Tk()
        root.title("Bo2LoZ Chatbot")
        txt = Text(root)
        txt.grid(row=0, column=0, columnspan=2)
        e = Entry(root, width=105)
        e.grid(row=1, column=0)
        send = Button(root, text="Send", command=sendfun).grid(row=1, column=1)
        inf = Button(root, text="History", command=info)
        inf.place(x=585, y=390)
        root.mainloop()
    elif user == "" and code == "":
        messagebox.showerror("invalid", "empty password and usermail")
    elif user == "":
        messagebox.showerror("invalid", "empty usermail")
    elif code == "":
        messagebox.showerror("invalid", "empty password")
    else:
        messagebox.showerror("invalid", "rong password or email")

def signup():
    global firstname
    global secondname
    global gend
    global old
    global mail
    global passw
    screen.destroy()
    print("signup")

    sign = Tk()
    sign.geometry("1280x720+150+70")
    sign.configure(bg='#d7dae2')
    sign.title("Signup Page")

    lbltitle = Label(text="Signup Page", font=("arial", 50, "bold"), fg="black", bg="#d7dae2")
    lbltitle.pack(pady=50)

    firstname = StringVar()
    secondname = StringVar()
    gend = StringVar()
    old = StringVar()
    mail = StringVar()
    passw = StringVar()

    first = Label(text="First Name", font=("arial", 30, "bold"), bg="#d7dae2")
    first.place(x=100, y=200)
    first = Entry(textvariable=firstname, width=12, bd=2, font=("arial", 30))
    first.place(x=400, y=200)

    second = Label(text="Second Name", font=("arial", 30, "bold"), bg="#d7dae2")
    second.place(x=100, y=300)
    second = Entry(textvariable=secondname, width=12, bd=2, font=("arial", 30))
    second.place(x=400, y=300)

    gender = Label(text="gender", font=("arial", 30, "bold"), bg="#d7dae2")
    gender.place(x=100, y=400)
    gender = Entry(textvariable=gend, width=12, bd=2, font=("arial", 30))
    gender.place(x=400, y=400)

    age = Label(text="Age", font=("arial", 30, "bold"), bg="#d7dae2")
    age.place(x=800, y=200)
    age = Entry(textvariable=old, width=12, bd=2, font=("arial", 30))
    age.place(x=950, y=200)

    email = Label(text="Email", font=("arial", 30, "bold"), bg="#d7dae2")
    email.place(x=800, y=300)
    email = Entry(textvariable=mail, width=12, bd=2, font=("arial", 30))
    email.place(x=950, y=300)

    password = Label(text="Pass", font=("arial", 30, "bold"), bg="#d7dae2")
    password.place(x=800, y=400)
    password = Entry(textvariable=passw, width=12, bd=2, font=("arial", 30), show="*")
    password.place(x=950, y=400)

    butt1 = Button(text="Save", height="3", width=23, bg="#ed3833", fg="white", bd=0, command=save)
    butt1.place(x=300, y=550)
    butt2 = Button(text="Exit", height="3", width=23, bg="#ed3833", fg="white", bd=0, command=sign.destroy)
    butt2.place(x=900, y=550)

    sign.mainloop()

def save():
    userfirstname = firstname.get()
    usersecondname = secondname.get()
    usergender = gend.get()
    userage = old.get()
    useremail = mail.get()
    userpassword = passw.get()
    print(userfirstname, usersecondname, usergender, userage, useremail, userpassword)
    sql="INSERT INTO user (Fname, Lname, gender, age, email, password) VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql,(userfirstname, usersecondname, usergender, userage, useremail, userpassword))
    db.commit()
    #print(mycursor.execute("INSERT INTO `user`(`Fname`, `Lname`, `gender`, `age`, `email`, `password`) VALUES (" + userfirstname + "," + usersecondname + "," + usergender + "," + userage + "," + useremail + "," + userpassword + ")"))
    print("saving")

def info():
    print("this is info")
    #mycursor.execute("select question,answer from info WHERE user_id =" + "'" + str(user_id) + "'")
    mycursor.execute("select question,answer from main WHERE user_id =" + "'" + str(user_id) + "'")
    vale = mycursor.fetchall()
    for v in vale:
        q,a = v
        print(q)
        print(a)
        txt.insert(END, "\n" + "bot : " + q )
        txt.insert(END, "\n" + "bot : " + a )

def sendfun():
    global que
    que = e.get()
    s = "you : " + e.get()
    print(user_id)
    txt.insert(END, "\n" + s)
    value, intent, confin1, entity1, confe1, entity2, confe2, entity3, confe3, entity4, confe4 = wit_response(e.get())
    respond(intent, entity1, entity2, entity3, entity4)
    print(wit_response(e.get()))
    check(confin1, confe1,confe2,confe3,confe4)
    e.delete(0, END)
    appear(user_id,intent, entity1, entity2, entity3, entity4, confin1, confe1, confe2, confe3, confe4)

def wit_response(message_text):
    resp = client.message(message_text)
    print(resp)
    value = None
    intent = None
    entity1 = None
    entity2 = None
    entity3 = None
    entity4 = None
    confin1 = None
    confe1 = None
    confe2 = None
    confe3 = None
    confe4 = None
    try:
        value = list(resp['entities'])[0]
        intent = resp.get("intents")[0].get("name")
        confin1 = float(resp.get("intents")[0].get("confidence"))
        entity1 = resp['entities'][value][0]['value']
        confe1 = float(resp['entities'][value][0].get("confidence"))
        entity2 = resp['entities'][value][1]['value']
        confe2 = float(resp['entities'][value][1].get("confidence"))
        entity3 = resp['entities'][value][2]['value']
        confe3 = float(resp['entities'][value][2].get("confidence"))
        entity4 = resp['entities'][value][3]['value']
        confe4 = float(resp['entities'][value][3].get("confidence"))
    except:
        pass
    return (value, intent, confin1, entity1, confe1, entity2, confe2, entity3, confe3, entity4, confe4)

def respond(intent, entity1, entity2, entity3, entity4):
    if intent == "greeding":
        txt.insert(END, "\n" + "bot : hello , how can i help you")
    elif intent == "bye":
        txt.insert(END, "\n" + "bot : bye , nice to meet you")
    elif intent == "distance":
        print("12")
        print(entity1)
        print(entity2)
        mycursor.execute(
            "select distance from distance WHERE country1 =" + "'" + entity1 + "'" + "and country2 = " + "'" + entity2 + "'")
        vale = mycursor.fetchall()
        for v in vale:
            a = v[0]
            print(a)
            txt.insert(END, "\n" + "bot : " + str(a))
    elif intent == "food":
        print("21")
        print(entity1)
        print(entity2)
        mycursor.execute(
            "select food from food WHERE country1 =" + "'" + entity1 + "'" + "and country2 = " + "'" + entity2 + "'")
        vale = mycursor.fetchall()
        for v in vale:
            a = v[0]
            print(a)
            txt.insert(END, "\n" + "bot : " + str(a))
    elif intent == "price":
        if entity1 != None:
            print("31")
            print(entity1)
            mycursor.execute("select price from price WHERE country =" + "'" + entity1 + "'")
            vale = mycursor.fetchall()
            for v in vale:
                a = v[0]
                print(a)
                txt.insert(END, "\n" + "bot : " + str(a))
        if entity2 != None:
            print("32")
            print(entity1)
            print(entity2)
            mycursor.execute("select price from price WHERE country =" + "'" + entity2 + "'")
            vale = mycursor.fetchall()
            for v in vale:
                a = v[0]
                print(a)
                txt.insert(END, "\n" + "bot : " + str(a))
        if entity3 != None:
            print("33")
            print(entity1)
            print(entity2)
            print(entity3)
            mycursor.execute("select price from price WHERE country =" + "'" + entity3 + "'")
            vale = mycursor.fetchall()
            for v in vale:
                a = v[0]
                print(a)
                txt.insert(END, "\n" + "bot : " + str(a))
        if entity4 != None:
            print("34")
            print(entity1)
            print(entity2)
            print(entity3)
            print(entity4)
            mycursor.execute("select price from price WHERE country =" + "'" + entity4 + "'")
            vale = mycursor.fetchall()
            for v in vale:
                a = v[0]
                print(a)
                txt.insert(END, "\n" + "bot : " + str(a))
    elif intent == "hotel":
        if entity1 != None:
            print("51")
            print(entity1)
            mycursor.execute("select name , no_star from hotel WHERE country =" + "'" + entity1 + "'")
            vale = mycursor.fetchall()
            for v in vale:
                a = v[0]
                print(a)
                txt.insert(END, "\n" + "bot : " + str(a))
        if entity2 != None:
            print("52")
            print(entity1)
            print(entity2)
            mycursor.execute("select name , no_star from hotel WHERE country =" + "'" + entity2 + "'")
            vale = mycursor.fetchall()
            for v in vale:
                a = v[0]
                print(a)
                txt.insert(END, "\n" + "bot : " + str(a))
        if entity3 != None:
            print("53")
            print(entity1)
            print(entity2)
            print(entity3)
            mycursor.execute("select name , no_star from hotel WHERE country =" + "'" + entity3 + "'")
            vale = mycursor.fetchall()
            for v in vale:
                a = v[0]
                print(a)
                txt.insert(END, "\n" + "bot : " + str(a))
        if entity4 != None:
            print("54")
            print(entity1)
            print(entity2)
            print(entity3)
            print(entity4)
            mycursor.execute("select name , no_star from hotel WHERE country =" + "'" + entity4 + "'")
            vale = mycursor.fetchall()
            for v in vale:
                a = v[0]
                print(a)
                txt.insert(END, "\n" + "bot : " + str(a))
    elif intent == "arrive":
        print("61")
        print(entity1)
        print(entity2)
        mycursor.execute(
            "select time from arrive WHERE country1 =" + "'" + entity1 + "'" + "and country2 = " + "'" + entity2 + "'")
        vale = mycursor.fetchall()
        for v in vale:
            a = v[0]
            print(a)
            txt.insert(END, "\n" + "bot : " + str(a))
    elif intent == "leave":
        print("71")
        print(entity1)
        print(entity2)
        mycursor.execute(
            "select time from land WHERE country1 =" + "'" + entity1 + "'" + "and country2 = " + "'" + entity2 + "'")
        vale = mycursor.fetchall()
        for v in vale:
            a = v[0]
            print(a)
            txt.insert(END, "\n" + "bot : " + str(a))
    else:
        txt.insert(END, "\n" + "bot : sorry , i dont know")

def check(confin1, confe1,confe2,confe3,confe4):
    global chi
    global che1
    global che2
    global che3
    global che4
    if confin1 > 0.7:
        print("confidence type of intent : " + "good")
        chi = "T"
    else:
        print("confidence type of intent : " + "bad")
        chi = "F"
        dist(que)
    if confe1 > 0.7:
        print("confidence type of entity1 : " + "good")
        che1 = "T"
    else:
        print("confidence type of entity1 : " + "bad")
        che1 = "F"
        dist(que)
    if confe2 != None:
            if confe2 > 0.7:
                print("confidence type of entity2 : " + "good")
                che2 = "T"
    else:
        print("confidence type of entity2 : " + "bad")
        che2 = "F"
    if confe3 != None:
        if confe3 > 0.7:
            print("confidence type of entity3 : " + "good")
            che3 = "T"
    else:
        print("confidence type of entity3 : " + "bad")
        che3 = "F"
    if confe4 != None:
        if confe4 > 0.7:
            print("confidence type of entity4 : " + "good")
            che4 = "T"
    else:
        print("confidence type of entity4 : " + "bad")
        che4 = "F"

def appear(user_id,intent, entity1, entity2, entity3, entity4, confin1, confe1, confe2, confe3, confe4):
    x = []
    bedo = 0
    print("user id is  : " + str(user_id))
    print("intent : " + intent)
    print("intent confidence  : " + str(confin1))
    if entity1 != None:
        print("entity1 : " + entity1)
        x.append(entity1)
    if confe1 != None:
        print("entity1 confidence : " + str(confe1))
    if entity2 != None:
        print("entity2 : " + entity2)
        x.append(entity2)
    if confe2 != None:
        print("entity2 confidence : " + str(confe2))
    if entity3 != None:
        print("entity3 : " + entity3)
        x.append(entity3)
    if confe3 != None:
        print("entity3 confidence : " + str(confe3))
    if entity4 != None:
        print("entity4 : " + entity4)
        x.append(entity4)
    if confe4 != None:
        print("entity4 confidence : " + str(confe4))
    while bedo < len(x):
        print("this is the : ", bedo, "entity : ", x[bedo])
        bedo = bedo + 1
    if entity2 == None:
        entity2=0
    if entity3 == None:
        entity3 = 0
    if entity4 == None:
        entity4 = 0
    if confe2 == None:
        confe2=0
    if confe3 == None:
        confe3=0
    if confe4 == None:
        confe4=0
    sql = "INSERT INTO information (user_id,question, intent ,conf_intent,status_intent,entity1,conf_entity1,status_entity1,entity2,conf_entity2,status_entity2,entity3,conf_entity3,status_entity3,entity4,conf_entity4,status_entity4) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql,(user_id,que,intent,confin1,chi,entity1,confe1,che1,entity2,confe2,che2,entity3,confe3,che3,entity4,confe4,che4))
    db.commit()

mainscreen()