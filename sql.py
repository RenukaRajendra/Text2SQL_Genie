import sqlite3
connection = sqlite3.connect("student.db")

cursor=connection.cursor()

table_info = """
create table STUDENT3(NAME VARCHAR(25), CLASS VARCHAR(25),SECTION VARCHAR(25), MARKS INT);
"""

cursor.execute(table_info)

cursor.execute('''Insert into STUDENT3 values('Renu','DataScience','A',90)''')
cursor.execute('''Insert into STUDENT3 values('Raj','DataScience','A',80)''')
cursor.execute('''Insert into STUDENT3 values('RRB','DataScience','A',70)''')
cursor.execute('''Insert into STUDENT3 values('Ramya','Devops','B',60)''')
cursor.execute('''Insert into STUDENT3 values('Lahari','Devops','A',70)''')

print("The inserted records are")

data = cursor.execute('''Select * from STUDENT3''')

for row in data:
    print(row)

connection.commit()
connection.close()