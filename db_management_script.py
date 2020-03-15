from mysql.connector import connect
from os import system
from time import sleep
d=None


def rem(x):
  chrs=['(', ')' , ',']
  temp=""
  for ch in x:
    if ch not in chrs:
      temp=temp+ch
  return temp

def menu(db):
  system("cls")
  print(f"\n\n\t\tHost:{db.h}\tUser:{db.u}\tDatabase:{db.d}")
  print("\n ________________________________________________________________________________ ")
  print("*                        MYsql Database Management Script v1.0                   *")
  print("*________________________________________________________________________________* - by Vaibhav Haswani\n\n")
  print("1) List Tables\n2) Create new table\n3) Table Description Operations\n4) Table Manipulation Operations \n5) More Operations\n6) Change Database\n7) Database Operations\n... Use q to exit ...")
  opt=input("Choose Option:")
  if opt=='1':
    system("cls")
    db.list_tables()
  elif opt=='2':
    system("cls")
    db.newTable()
  elif opt=='3':
    system("cls")
    db.ddlTable()
  elif opt=='4':
    pass
  elif opt=='5':
    pass
  elif opt=='6':
    system("cls")
    db.changeDatabase()
  elif opt=='7':
    system("cls")
    db.databaseMod()
  elif opt=='q' or opt=='Q':
    exit()
  else:
    print("... Enter a valid option ...")
    menu(db)



def main():
  global d
  host=input("Enter Host name:")
  user=input("Enter User name:")
  pas=input("Enter Password:")
  dn=input("Enter database to use:")
  d=database(host,dn,user,pas)
  menu(d)


class database:

  def __init__(self,h,d,u,p):
    try:
      self.con=connect(host=h,database=d,user=u,password=p)
      self.h,self.d,self.u,self.p=h,d,u,p
      self.cursor=self.con.cursor()
      print("..Connected to Database...")
      sleep(3)


    except:
      print("...Check Your Credentials and RETRY...")
      main()



  def des_frame(self,tl): #description frame
    for row in tl:
      print("-----------------------------------------------------------------------------------------")
      for col in row:
        print(f"|    {col}    |",end="")
      print()
      print("-----------------------------------------------------------------------------------------")


  def databaseMod(self):
    try:
      print("List of available databases:")
      self.cursor.execute("show databases")
      dl=list(map(rem,self.cursor.fetchall()))
      for i in range(len(dl)):
        print(f"{i}) {dl[i]}")

      print("\n\nAvailable options:\na) Create New database\nb) Drop a database")
      ch=input("Choose Option:")
      if ch=='a':
        db=input("enter name of database you want to create:")
        self.cursor.execute(f"create database {db}")
        print(".. Database created successfully ..")
      elif ch=='b':
        db=input("enter name of database you want to drop:")
        self.cursor.execute(f"drop database {db}")
        print(".. Database dropped successfully ..")
      else:
        print("..Not a valid option..")

    except:
      print(".. Can't update database list..")
    ch=input(".. press 1 to return to main menu ..")
    if ch=='1':
      global d
      menu(d)



  def changeDatabase(self):
    try:
      print("List of available databases:")
      self.cursor.execute("show databases")
      dl=list(map(rem,self.cursor.fetchall()))
      for i in range(len(dl)):
        print(f"{i}) {dl[i]}")
      db=input("Enter database name you want to switch:")
      self.con=connect(host=self.h,database=db,user=self.u,password=self.p)
      self.cursor=self.con.cursor()
      self.d=db
      print(".. Database Switched ..")

    except:
      print(".. Can't access or can't switch databases ..")
    ch=input(".. press 1 to return to main menu ..")
    if ch=='1':
      global d
      menu(d)


  def list_tables(self):
    try:
      global d
      self.cursor.execute("show tables")
      table=list(map(rem,self.cursor.fetchall()))
      for i in range(len(table)):
        print(f"{i}) {table[i]}")
    except:
      print("... No record Found ...")
    choice=int(input("Choose 1 to describe specific table and 0 to return to main menu:"))
    if choice==1:
      self.describe()
    elif choice=='0':
      menu(d)




  def newTable(self):
      try:
        tn=input("Enter table name:")
        n=int(input("enter no of columns you want to add:"))
        cl=""
        print(".. Label columns ..")
        for i in range(n):
          cn=input(f"Enter column {i} name:")
          dt=input("Enter datatype(varchar(n),int,date etc.):")
          if cl=="":
            cl=cl+f"{cn} {dt}"
          else:
            cl=cl+f", {cn} {dt}"
        self.cursor.execute(f"create table {tn}( {cl} )")
        print(".. Table created successfully ..")

      except:
        print("...Can't create table...")
      ch=input(".. press 1 to return to main menu ..")
      if ch=='1':
        global d
        menu(d)



  def describe(self):

    tn=input("Enter table name(for description):")
    try:
      self.cursor.execute(f"describe {tn}")
      c=self.cursor.fetchall()
      self.des_frame(c)
    except:
      print("... No Table found ...")
    ch=input(".. press 1 to return to main menu ..")
    if ch=='1':
      global d
      menu(d)




  def ddlTable(self):
    try:
      global d
      self.cursor.execute("show tables")
      table=list(map(rem,self.cursor.fetchall()))
      for i in range(len(table)):
        print(f"{i}) {table[i]}")
    except:
      print("... No record Found ...")
      return
    tn=input("Enter table name to select:")
    print("a) Drop table\nb) Alter table\nc) Rename table")
    opt=input("Choose Option:")

    try:
      if opt=='a':
        self.cursor.execute(f"drop table {tn}")
        print("...Table Dropped...")
        #options to add
      else:
        print("...Invalid Option...")
    except:
        print("...DDL Exeption...")
    ch=input(".. press 1 to return to main menu ..")
    if ch=='1':
      global d
      menu(d)






if __name__=="__main__":
  main()



