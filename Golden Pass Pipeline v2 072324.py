#imports
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

#requests - found by inspecting the page elements
r=requests.get("http://www.gasnom.com/ip/GOLDENPASS/oauc.cfm?type=1")
webpage=bs(r.content, features="lxml")

#determine column names
table = webpage.select("div.row")[0].select("table")[1].select("tr")[0] #targets the tr tag containing the headers
col=[]
for tag in table.find_all("td"):
	col.append(tag.text.replace("\r\n","").lstrip().rstrip()) #removes the \r\n occurrences and whitespaces that happen only in the OAC column

#accommodate the blank space at the end of each row (i.e. rows have an extra empty cell at the end)
col.append("") 

#collect row data
table5 = webpage.select("div.row")[0].select("table")[1].select('td[class^="datacell"]') #targets the table contents
row5=[]
for tag in table5:
	row5.append(tag.text.replace("\r\n","").lstrip().rstrip()) #removes the \r\n occurrences and whitespaces in many of the columns

#convert flat list into list of lists
num_columns = len(col)
rows = [row5[i:i + num_columns] for i in range(0, len(row5), num_columns)]

#convert into pandas dataframe
df=pd.DataFrame(rows,columns=col)
#print(df.to_string())

#Finally write pandas to CSV
df.to_csv('results4.csv')
