import json
import sqlite3
from enum import Enum

class Roles(Enum):
  Student = 0
  Teacher = 1
  NonDefined = 2

con = sqlite3.connect("rousterdb.sqlite")
cur = con.cursor()

cur.executescript('''
DROP TABLE if exists User;
DROP TABLE if exists Course;
DROP TABLE if exists member;

CREATE TABLE User ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
					'name' TEXT UNIQUE, 'Role' INTEGER);
CREATE TABLE Course ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
					 'title' TEXT UNIQUE);
CREATE TABLE Member ('user_id' INTEGER, 'course_id' INTEGER, PRIMARY KEY('user_id','course_id'));					 
					''')

#This method convert integer roles to string (0->Student, 1->Teacher)
def convertIntegerRoleToString(role):
  if role==0:
    return Roles.Student.name
  elif role==1:
    return Roles.Teacher.name
  else:
     return Roles.NonDefined.name

fName = input("Enter file name: ")
if len(fName)<1:
  fName = 'roster_data_sample.json'
print()

str_data = open(fName).read()
#Parsing the json file
json_data = json.loads(str_data)
print('User_Name,','Role,','Course_Title')
for element in json_data:
  name = element[0]
  title = element[1]
  role = element[2]
  print((name,convertIntegerRoleToString(role),title))

  #Insert data DB
  cur.execute('''insert or ignore into User (name,role) values (?,?)''',(name,role))
  cur.execute('''select id from User where name=? ''',(name,))
  user_id = cur.fetchone()[0]

  cur.execute('''insert or ignore into Course (title) values (?)''',(title,))
  cur.execute('''select id from Course where title=? ''',(title,))
  course_id = cur.fetchone()[0]

  cur.execute(''' insert into Member (user_id,course_id) values (?,?)''',(user_id,course_id))

  con.commit()