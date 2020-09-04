import sqlite3

#Create a DB
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

#Drop the DB if it already exist
cur.execute('DROP TABLE IF EXISTS Counts')

#Create Table counts to caculate number of each email address
cur.execute('CREATE TABLE Counts (email TEXT, count INTEGER)')

#Read a txt file
fname = input('Enter file name: ')
if (len(fname)<1):
  fname = 'mbox-short.txt'

fhandle = open(fname)
#this for loop read each line of the txt file and if it starts with 'From:', then adds the email to the Counts table
for line in fhandle:
  line.strip()
  if not line.startswith('From:'):
    continue
  llist= line.split()
  email = llist[1]
  #print('')
  #print(email)
  cur.execute('select count from Counts where email = ?',(email,))
  row = cur.fetchone()
  if row is None:
    cur.execute('INSERT INTO Counts (email,count) VALUES (?,1)', (email,))
  else:
    cur.execute('UPDATE Counts SET count = count+1 WHERE email = ?',(email,))
  #Save changes in DB
  conn.commit()

sqlstr =cur.execute('select * FROM Counts ORDER BY count DESC LIMIT 10')
for row in sqlstr:
  print('email addr is: ', str(row[0]), ', Count: ', row[1])
  
cur.close()

 