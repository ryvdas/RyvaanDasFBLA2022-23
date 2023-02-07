import json
from tkinter import *

root = Tk()
root.geometry("1000x1000")

enteredInfo = {'grade': '', 'quarter': ''}

def generate_report():
    with open('studentPoints.json', 'r') as info_file:
        info = json.load(info_file)
    gradeData = info[(int(enteredInfo['grade'])-9)]
    gradeStudents = gradeData['students']
    key = 'q' + enteredInfo['quarter'] + 'Points'
    namePointsDict = {}
    for i in gradeStudents:
        namePointsDict[i['name']] = i[key]
    dataRoot = Tk()
    dataRoot.geometry('300x1000')
    sortedNamesByPoints = sorted(namePointsDict.items(), key=lambda x:x[1], reverse=True)
    for i in sortedNamesByPoints:
        # ('charles hess', 10)
        name=i[0]
        # 'charles hess'
        name = name.split(' ')
        # ['charles', 'hess']
        for j in range(len(name)):
            name[j] = name[j].capitalize()
        points=i[1]
        labeltxt = name[0] + ' '+ name[1] + ': ' + str(points)
        Label(dataRoot, text=labeltxt).pack()
# drop down with all 4 grades
def quarter_chosen():
    q = qclicked.get()
    enteredInfo['quarter'] = q
    gOptions = ['9', '10', '11', '12']
    gclicked = StringVar()
    gclicked.set('Choose Grade')
    gradePicker = OptionMenu(root, gclicked, *gOptions).pack(pady=20)
    def grade_chosen():
        g = gclicked.get()
        enteredInfo['grade'] = g
        generate_report()
    enterButton = Button(root, text="Generate Report", command=grade_chosen).pack(pady=20)
    
    

qOptions = ['1', '2', '3', '4']
qclicked = StringVar()
qclicked.set('Choose Quarter')
quarterPicker = OptionMenu(root, qclicked, *qOptions).pack(pady=20)

enterButton = Button(root, text="Enter", command=quarter_chosen).pack()

root.mainloop()