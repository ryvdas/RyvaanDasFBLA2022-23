import json
from tkinter import *
from tkcalendar import Calendar

# tk init

root = Tk()
root.geometry("1000x1000")
cal = Calendar(root, selectmode = 'day', year = 2023)
cal.pack(pady = 20)

# Loading files into program
def load_all_files():
    with open('rewards.json') as rewards_file:
        rewardsData = json.load(rewards_file)

    with open('studentEventAttendance.json') as studentEventAttendanceFile:
        studentEventAttendanceData = json.load(studentEventAttendanceFile)

    with open('studentPoints.json') as studentPointsFile:
        studentPointsData = json.load(studentPointsFile)

    with open('quarterlyEvents.json') as quarterlyEventsFile:
        quarterlyEventsData = json.load(quarterlyEventsFile)

def event_date():  # Get event's date from date picker and store it in JSON file
    eventDate = cal.get_date()
    with open('enteredInfo.json', 'r') as info_file:
        info = json.load(info_file)
    with open('enteredInfo.json', 'w') as info_file:
        info["eventDate"] = eventDate
        info_file.truncate()
        json.dump(info, info_file, indent=4)

def retrieve_student_name_input():
    inputValue = studentNameTextBox.get("1.0", "end-1c")
    inputValue = inputValue.upper()
    inputValue = inputValue.lower()
    with open('enteredInfo.json', 'r') as info_file:
        info = json.load(info_file)
    with open('enteredInfo.json', 'w') as info_file:
        info["studentName"] = inputValue
        info_file.truncate()
        json.dump(info, info_file, indent=4)
        
def retrieve_student_id_input():
    inputValue = studentIDtextBox.get("1.0", "end-1c")
    inputValue = inputValue.upper()
    inputValue = inputValue.lower()
    with open('enteredInfo.json', 'r') as info_file:
        info = json.load(info_file)
    with open('enteredInfo.json', 'w') as info_file:
        info["studentID"] = inputValue
        info_file.truncate()
        json.dump(info, info_file, indent=4)

# award points to student
def award_points():
    
    def split_date_list(s):
        l = s.split('/')
        return l

    def change_date_to_ISO(l):
        d = "20"
        d = d + l[2] + '-'
        if len(l[0]) == 2:
            d = d + l[0] + '-'
        elif len(l[0]) == 1:
            d = d + '0' + l[0] + '-'
        if len(l[1]) == 1:
            d = d + '0' + l[1]
        elif len(l[1]) == 2:
            d = d + l[1]
        return d

    with open('enteredInfo.json', 'r') as info_file:
        info = json.load(info_file)
        eventDate = info['eventDate']
        studentName = info['studentName']
        studentID = info['studentID']
        eventType = info['eventType']
        eventName = info['eventName']
        enteredDate = change_date_to_ISO(split_date_list(eventDate))
    # find the quarter the event is in
    with open('quarterDates.json', 'r') as info_file:
        info = json.load(info_file)
        q1date = change_date_to_ISO(split_date_list(info['q1']))
        q2date = change_date_to_ISO(split_date_list(info['q2']))
        q3date = change_date_to_ISO(split_date_list(info['q3']))
        q4date = change_date_to_ISO(split_date_list(info['q4']))
    if enteredDate < q4date:
        quarter = 'q4'
        if enteredDate < q3date:
            quarter = 'q3'
            if enteredDate < q2date:
                quarter = 'q2'
                if enteredDate < q1date:
                    quarter = 'q1'
    
    # award the point
    with open('studentPoints.json', 'r') as info_file:
        info = json.load(info_file)
        for i in info:
            students = i['students']
            for j in students:
                # check name
                if studentName == j['name']:
                    # check id
                    if studentID == j['id']:
                        # change point in specific quarter
                        quarter = quarter + "Points"
                        j[quarter] = j[quarter] + 1
    with open('studentPoints.json', 'w') as info_file:
        info_file.truncate()
        json.dump(info, info_file, indent = 4)
        
    awarded = False

    with open('studentPoints.json', 'r') as info_file:
        info = json.load(info_file)
        for i in info:
            students = i['students']
            for j in students:
                # check name
                if studentName == j['name']:
                    # check id
                    if int(studentID) == j['id']:
                        # change point in specific quarter
                        quarter = quarter + "Points"
                        j[quarter] = j[quarter] + 1
                        awarded = True
                        for widget in root.winfo_children():
                            widget.destroy()
                        Label(root, text="Thank you! You may now close this window.").pack()

    with open('studentPoints.json', 'w') as info_file:
        info_file.truncate()
        json.dump(info, info_file, indent = 4)
    
    if awarded == False:
        for widget in root.winfo_children():
            widget.destroy()
        Label(root, text="There was no student found with a matching name and student ID. Please close this window and re-enter the information")
    
    

# clear entered info
with open('enteredInfo.json', 'r') as info_file:
    info = json.load(info_file)
    info['eventDate'] = ""
    info['studentName'] = ""
    info['studentID'] = ""
    info['eventType'] = ""
    info['eventName'] = ""
with open('enteredInfo.json', 'w') as info_file:
    info_file.truncate()
    json.dump(info, info_file, indent=4)
    
# Date picker
Button(root,text = "Get Date", command = event_date).pack()

# Student name text box
studentNameLabel = Label(root, text="Enter your name below.")
studentNameLabel.pack(pady=10)
studentNameTextBox = Text(root, height = 2, width = 10)
studentNameTextBox.pack()
studentNameButton = Button(root, height=1, width=10, text="Enter", command = retrieve_student_name_input)
studentNameButton.pack()

# Student ID text box
studentIDLabel = Label(root, text="Enter your student number below.")
studentIDLabel.pack(pady=10)
studentIDtextBox = Text(root, height = 2, width = 10)
studentIDtextBox.pack()
studentIDButton = Button(root, height=1, width=10, text="Enter", command = retrieve_student_id_input)
studentIDButton.pack()

def sel():
    selection = "You selected "+str(v.get()) + "."
    label.config(text=selection)
    with open("enteredInfo.json", 'r') as info_file:
        info = json.load(info_file)
    with open("enteredInfo.json", 'w') as info_file:
        if v.get() == "Sporting Event":
            info["eventType"] = "Sporting"
        else:
            info["eventType"] = "Non-Sporting"
        info_file.truncate()
        json.dump(info, info_file, indent=4)
        
    
sporting = True
v = StringVar(root)
sportingRButton = Radiobutton(root, text = "Sporting Event", variable = v,value = "Sporting Event", command = sel).pack(side = TOP)
nonsportingRButton = Radiobutton(root, text = "Non-Sporting Event", variable = v,value = "Non-Sporting Event", command = sel).pack()
label = Label(root)
label.pack()

# create next button
#nextButtonPressed = False

def next_button_pressed():
    # check to see if all data is entered
    with open('enteredInfo.json', 'r') as info_file:
        info = json.load(info_file)
        toReEnter = []
        reEnter = False
        # check eventDate
        if info['eventDate'] == "":
            toReEnter.append('Event Date')
            reEnter = True
        # check studentName
        if info['studentName'] == "":
            toReEnter.append('Student Name')
            reEnter = True
        # check studentID
        if info['studentID'] == "":
            toReEnter.append('Student ID')
            reEnter = True
        # Check eventType
        if info['eventType'] == "":
            toReEnter.append('Event Type')
            reEnter = True
        if reEnter:
            txt = "Please enter the following information: "
            for i in toReEnter:
                txt = txt + i + ', '
            txt = txt[0:-2]
            txt = txt + '.'
            l = Label(root, text=txt).pack()
            
    if reEnter == False:
        # find events in that category
        with open("event.json", 'r') as info_file:
            eventInfo = json.load(info_file)
        with open("enteredInfo.json", 'r') as info_file:
            enteredInfo = json.load(info_file)
        # if event is sport, look at 1st (0 index) or, look at 2nd, (1 index)
        if enteredInfo["eventType"] == "Sporting":
            currentEvents = eventInfo[0]['events']
        elif enteredInfo["eventType"] == "Non-Sporting":
            currentEvents = eventInfo[1]['events']
        correctEvents = []
        date = enteredInfo["eventDate"]
        for i in currentEvents:
            currentDict = i
            if currentDict['date'] == date:
                # create new info storing dict
                newDict={}
                newDict['id'] = currentDict['id']
                newDict['name'] = currentDict['name']
                correctEvents.append(newDict)
        if len(correctEvents) == 0:
            label = Label(root, text="There are no events found. Please check that you have entered the date and event type correctly.")
            label.pack()
        else:
            # create dropdown menu
            def show():
                chosen = clicked.get()
                label.config(text=chosen)
                with open("enteredInfo.json", 'r') as info_file:
                    info = json.load(info_file)
                    info['eventName'] = chosen
                with open("enteredInfo.json", 'w') as info_file:
                    info_file.truncate()
                    json.dump(info, info_file, indent=4)

            clicked=StringVar()
            options = []
            for i in correctEvents:
                eventName = i['name']
                options.append(eventName)
            clicked.set("Choose Event")
            dropmenu = OptionMenu(root, clicked, *options)
            dropmenu.pack()
            enterButton = Button(root, text="Enter", command=show).pack()
            label=Label(root, text="")
            label.pack()
            spacefiller = Label(root, text="").pack()
            def submit_button_pressed():
                for widget in root.winfo_children():
                    widget.destroy()
                label = Label(root, text="Loading...").pack()
                award_points()
            submitButton = Button(root, text="Submit", command = submit_button_pressed).pack()
        

nextButton = Button(root, command=next_button_pressed, text = "Next>>>").pack()

root.mainloop()