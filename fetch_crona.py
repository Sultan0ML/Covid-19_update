import urllib
from bs4 import BeautifulSoup
import sqlite3
from tkinter import*
import datetime

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


url='https://akashraj.tech/corona/world?r=work'
def global_data():
    url='https://akashraj.tech/corona/world?r=work'
    json_obj = urllib.request.urlopen(url)
    soup=BeautifulSoup(json_obj,"xml")
    glob=soup.find('div',class_='row my-2')
    output=''
    for i in glob.find_all('span',class_="m-auto font-weight-bold"):
        output=output+i.text
    return output

def creatdb():
    
    db=sqlite3.connect('covidData.db')
    db.execute('''CREATE TABLE IF NOT EXISTS covid(country TEXT NOT NULL,
                                    totalcase INT NOT NULL,
                                   death INT NOT NULL,
                                   activecase INT NOT NULL,
                                   recovered INT NOT NULL,
                                   newdeath INT NOT NULL,newcase INT NOT NULL)''')    
creatdb()

def insert(url):
   
    json_obj = urllib.request.urlopen(url)


    soup=BeautifulSoup(json_obj,"xml")
    
    datas=soup.find('div',id='result-holder')

    for item in datas.find_all('div',class_='card stats-card'):
        country=item.h3.text
        totalcase=item.h6.text
        death=item.find('div',class_='col death-cases').h4.text
        activecase=item.find('div',class_='col active-cases').h4.text
        recovered=item.find('div',class_='col recovered-cases').h4.text
        
        newdeath=item.find('h6',class_='card-title font-weight-bold text-danger').text
        newcase=item.find('div',class_="card-body p-1 text-center hidden-stats")
        for i in newcase.find_all('div',class_="col death-cases"):
            newcase=i.find('h6',class_='card-title font-weight-bold text-danger').text
        db=sqlite3.connect('covidData.db')

        db.execute('''INSERT INTO covid(country,totalcase,death,activecase,
                                      recovered,newdeath,newcase) VALUES(?,?,?,?,?,?,?)''',(country,totalcase,death,activecase,recovered,newdeath,newcase))
        db.commit()
insert(url)

  
def read_data(x):
    db=sqlite3.connect('covidData.db')

    data=db.execute('''SELECT * FROM covid WHERE country = ? COLLATE NOCASE ''',(x,))
    output=""
    for record in data:
        output=output +"Country :" +str(record[0])+"\n"+ "TotalCase:"+str(record[1])+"\n"+ "Death :"+ str(record[2]) +"\n"+"ActiveCase :" +str(record[3])+"\n"+"Recovered :" +str(record[4])+"\n"+"NewDeath :" +str(record[5])+"\n"+"NewCase :" +str(record[6])
        break
    return output
def closedb():
    connection  = sqlite3.connect("covidData.db")
    # Get a cursor object
    cursor= connection.cursor()
    # Execute the DROP Table SQL statement
    dropTableStatement = "DROP TABLE covid"
    #print("Table drop")
    cursor.execute(dropTableStatement)
    # Close the connection object
    return connection.close()


def refresh():
    closedb()
    creatdb()
    insert(url)
    #print("updated database")   
def showDate():
    now = datetime.datetime.now()
    msg = 'Today is: {}'.format(now)
    return msg




def detect():
    user_input = input1.get()
    features =read_data(user_input)
    answer.config(text=features)
root = Tk()
root.title('COVID-19 DATA')
root.geometry("650x350")
root.resizable(width=False, height=False)
root.configure(background='red')
topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)
x=showDate()
label1 = Label(topFrame, text=x)
label1.pack()
label1 = Label(topFrame, fg='white',bg='black',text="GLOBAL COVID-19 DATA")
label1.pack()
x=global_data()
label1 = Label(topFrame, text=x)
label1.pack()
label1 = Label(topFrame, text="Enter Country Name")
label1.pack()
input1 = Entry(topFrame)
input1.pack()
but=Button(topFrame, text='Search',bg='black',fg='white', command=detect)
but.pack()
but2=Button(topFrame, text='Refresh',bg='Blue',fg='white', command=refresh)
but2.pack()
button2 = Button(bottomFrame, text='Quit',fg='red',bg='white', command=root.quit)
button2.pack()
answer = Label(topFrame, text='')
answer.pack()
root.mainloop()
closedb()

