import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'localhost,1433' 
database = 'master' 
username = 'sa' 
password = 'Kislay631' 
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=no;UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


cursor.execute("SELECT * FROM [dbo].[spt_monitor];") 
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()