# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 21:43:56 2024

@author: crist
"""
import pypyodbc as odbc
import pyodbc
import pandas as pd

#df = pd.read_csv("c:\\user\\username\department.csv")
connection='Driver={ODBC Driver 18 for SQL Server};Server=server-web-submit.database.windows.net;Database=BD_web_submit;Uid=Parro;Pwd=Callelepanto12'
server = 'server-web-submit' 
database = 'BD_web_submit' 
username = 'Parro' 
password = 'Callelepanto12' 
cnxn = odbc.connect(connection)
"""
cursor = cnxn.cursor()
#Insert Dataframe into SQL Server:
#for index, row in df.iterrows():
cursor.execute("INSERT INTO Persons (PersonID,FirstName,LastName,Adress,City) values(?,?,?,?,?)", 2, 'David', 'Lopez','Solana','Madrid')
cnxn.commit()
cursor.close() 
"""
sql='''
SELECT *
FROM Persons
'''
cursor = cnxn.cursor()
cursor.execute(sql)
data=cursor.fetchall()

cursor.execute("INSERT INTO Persons (PersonID,FirstName,LastName,Address,City) VALUES (2, 'David', 'Lopez','Solana','Madrid')")
cursor.commit()
cursor.close() 