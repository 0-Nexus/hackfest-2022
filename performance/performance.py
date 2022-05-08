# Module Imports
import mariadb
import sys
import matplotlib.pyplot as plt
import numpy as np

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        port=3306,
        database="student"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
marks=[]
name=input("Enter student name: ")
for i in range(1,5):
    cur.execute(
        f'select q{i}.english,q{i}.history,q{i}.geography,q{i}.maths,q{i}.science from student_details, q{i}  where student_details.rollno=q{i}.rollno and name="{name}";'
    )
    marks.append(list(cur))
x=np.asarray(range(1,6,1))
y1=np.asarray(marks[0][0])
y2=np.asarray(marks[1][0])
y3=np.asarray(marks[2][0])
y4=np.asarray(marks[3][0])
fig,ax=plt.subplots(2,2,sharex='col',sharey='row')
ax[0][0].plot(x,y1)
ax[0][1].plot(x,y2)
ax[1][0].plot(x,y3)
ax[1][1].plot(x,y4)

plt.show()


