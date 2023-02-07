import json
from tkinter import *
import random

root = Tk()
root.geometry("1000x1000")

def update_rewards():
    with open("studentPoints.json", 'r') as info_file:
        studentPoints = json.load(info_file)
    with open("rewards.json", 'r') as info_file:
        rewards = json.load(info_file)
        
    # find points for each reward
    rewardAmounts = {}
    rewards = rewards["rewards"]
    for i in rewards:
        rewardName = i["name"]
        rewardPoints = i["points"]
        rewardAmounts[rewardName] = rewardPoints
        
    school = rewardAmounts['school reward']
    food = rewardAmounts['food reward']
    schoolSpirit = rewardAmounts['school spirit reward']
    
    # loop through students
    for i in studentPoints: 
        currentStudents = i["students"]
        for j in currentStudents:
            totalPoints = j["q1Points"] + j["q2Points"] + j["q3Points"] + j["q4Points"]
            reward = ""
            if totalPoints >= school:
                reward = "school reward"
                if totalPoints >= food:
                    reward = "food reward"
                    if totalPoints >= schoolSpirit:
                        reward = "school spirit reward"
            j["reward"] = reward
    with open("studentPoints.json", 'w') as info_file:
        info_file.truncate()
        json.dump(studentPoints, info_file, indent=4)

def show_rewards():
    update_rewards()
    rewardScreen = Tk()
    rewardScreen.geometry("500x1000")
    with open('studentPoints.json', 'r') as info_file:
        studentPoints = json.load(info_file)
        grades = ['9th Grade', '10th Grade', '11th Grade', '12th Grade']
    for i in studentPoints:
        currentStudents = i["students"]
        grade = i["grade"]
        Label(rewardScreen, text=grades[grade-9]).pack(anchor='w')
        for j in currentStudents:
            if j["reward"] != "":
                txt = j["name"] + ': ' + j["reward"]
            else:
                txt = j["name"] + ': no reward'
            Label(rewardScreen, text=txt).pack(anchor='w')
        
def pick_random_winners_by_grade(grade):
    with open('studentPoints.json', 'r') as info_file:
        info = json.load(info_file)
    students = info[(grade-9)]["students"]
    qList = ['q1', 'q2', 'q3', 'q4']
    winners = {}
    for i in range(4):
        # find people who scored points that quarter
        contestants = []
        for j in range(len(students)):
            currentStudent = students[j]
            key = qList[i] + 'Points'
            quarterPoints = currentStudent[key]
            if quarterPoints > 0:
                contestants.append(currentStudent["name"])
        # pick winner from contestants
        
        if len(contestants) == 1:
            winners[qList[i]] = contestants[0]
        elif len(contestants) == 0:
            winners[qList[i]] = "none"
        else:
            index = random.randint(0, (len(contestants)-1))
            winners[qList[i]] = contestants[index]
        
    return winners

def pick_random_winners():
    grade9Dict = pick_random_winners_by_grade(9)
    grade10Dict = pick_random_winners_by_grade(10)
    grade11Dict = pick_random_winners_by_grade(11)
    grade12Dict = pick_random_winners_by_grade(12)
    
    quarters = ['Quarter 1', 'Quarter 2', 'Quarter 3', 'Quarter 4']
    
    randomWinnersRoot = Tk()
    randomWinnersRoot.geometry('500x1000')
    
    Label(randomWinnersRoot, text='9th Grade: ').pack(anchor='w')
    for i in range(4):
        key = 'q' + str(i+1)
        currentWinner = grade9Dict[key]
        labelTxt = quarters[i] + ': ' + currentWinner
        Label(randomWinnersRoot, text=labelTxt).pack(anchor='w')
    
    Label(randomWinnersRoot, text='').pack()
    Label(randomWinnersRoot, text='9th Grade: ').pack(anchor='w')
    
    for i in range(4):
        key = 'q' + str(i+1)
        currentWinner = grade9Dict[key]
        labelTxt = quarters[i] + ': ' + currentWinner
        Label(randomWinnersRoot, text=labelTxt).pack(anchor='w')
    
    Label(randomWinnersRoot, text='').pack()
    Label(randomWinnersRoot, text='10th Grade: ').pack(anchor='w')
    
    for i in range(4):
        key = 'q' + str(i+1)
        currentWinner = grade10Dict[key]
        labelTxt = quarters[i] + ': ' + currentWinner
        Label(randomWinnersRoot, text=labelTxt).pack(anchor='w')
    
    Label(randomWinnersRoot, text='').pack()
    Label(randomWinnersRoot, text='11th Grade: ').pack(anchor='w')
    
    for i in range(4):
        key = 'q' + str(i+1)
        currentWinner = grade11Dict[key]
        labelTxt = quarters[i] + ': ' + currentWinner
        Label(randomWinnersRoot, text=labelTxt).pack(anchor='w')
    
    Label(randomWinnersRoot, text='').pack()
    Label(randomWinnersRoot, text='12th Grade: ').pack(anchor='w')
    
    for i in range(4):
        key = 'q' + str(i+1)
        currentWinner = grade12Dict[key]
        labelTxt = quarters[i] + ': ' + currentWinner
        Label(randomWinnersRoot, text=labelTxt).pack(anchor='w')

def find_top_students():
    with open('studentPoints.json', 'r') as info_file:
        info = json.load(info_file)

    grades = ['9th Grade', '10th Grade', '11th Grade', '12th Grade']
    
    topStudentsRoot = Tk()
    topStudentsRoot.geometry('500x1000')
    
    for i in range(4):
        students = info[i]["students"]
        totalStudentPoints = {}
        for j in students:
            totalPoints = j["q1Points"] + j["q2Points"] + j["q3Points"] + j["q4Points"]
            totalStudentPoints[str(j["name"])] = totalPoints

        totalStudentPoints = dict(sorted(totalStudentPoints.items(), key=lambda x:x[1], reverse=True))
        
        labelTxt = ''
        winnerName = list(totalStudentPoints.keys())[0]
        if totalStudentPoints[winnerName] > 0:
            labelTxt = grades[i] + ': ' + winnerName + ', ' + str(totalStudentPoints[winnerName])
        elif totalStudentPoints[winnerName] == 0:
            labelTxt = grades[i] + ': ' + 'No points were earned'
        
        Label(topStudentsRoot, text=labelTxt).pack()

showRewardsButton = Button(root, text='Update Rewards', command=show_rewards).pack()
pickRandomWinnersButton = Button(root, text='Pick Random Winners', command = pick_random_winners).pack()
topPointsButton = Button(root, text='Find Top Students', command=find_top_students).pack()
root.mainloop()