#imports
import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd

#requests - found by inspecting the page elements
r=requests.get("http://www.gasnom.com/ip/GOLDENPASS/oauc.cfm?type=1")
webpage=bs(r.content, features="html.parser")

#determine column names
table = webpage.select("div.row")[0].select("table")[1].select("tr")[0]
columns = table.find_all("td")
col=[]
for i in columns:
	pattern="<td\s*[^>]*>\s*.*?\s*<\/td\s*>"
	match_results=re.search(pattern,str(i))
	header=match_results.group()
	header=re.sub("<.*?>","",header)
	header=re.sub("\r\n","",header)
	header=re.sub("\s*","",header) #strips away all spaces, including those in cells, but solves the error message thrown by the "OAC" column header
	col.append(header)

#accommodate the blank space at the end of each row (i.e. rows have an extra empty cell at the end)
col.append("") 

#collect row data
table5 = webpage.select("div.row")[0].select("table")[1].select('td[class^="datacell"]')
row5=[]
for i in table5:
	pattern="<td\s*[^>]*>\s*.*?\s*<\/td\s*>"
	match_results=re.search(pattern,str(i))
	header=match_results.group()
	header=re.sub("<.*?>","",header)
	header=re.sub("\r\n","",header)
	header=re.sub("\s*","",header)
	row5.append(header)

#convert flat list into list of lists
num_columns = len(col)
rows = [row5[i:i + num_columns] for i in range(0, len(row5), num_columns)]

#convert into pandas dataframe
df=pd.DataFrame(rows,columns=col)
print(df.to_string())
