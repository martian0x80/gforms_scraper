from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import tempfile
import sys
import gsearch
import webbrowser
temp=tempfile.TemporaryFile(mode='w+t')
ques=[]
st_query=[]
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
headers = {"user-agent" : MOBILE_USER_AGENT}
d =  requests.get("https://docs.google.com/forms/d/e/1FAIpQLSc-0yT13LJNwE5VHTu10_f6xf49eznkDpuCT7h-s-oW4dcW2Q/viewform",headers=headers)
soup=BeautifulSoup(d.content.decode('utf-8'),'html.parser')
totalpage=soup.find(class_='freebirdFormviewerViewItemList')
tr_ques=totalpage.find_all(class_='freebirdFormviewerViewItemsItemItemTitleContainer')
for i in tr_ques:
	lines = i.get_text().encode('ascii','ignore')
	ques.append(lines)
#print(ques)
for j in range(0,len(ques)):
	if j!='':
		pretty = ques[j]
		data = (pretty+' ')
		temp.write(data)
		print(data, file=sys.stdout, sep=',')
	else:
		del ques[j]
print('+---------------------------------------------------------------------------------------------------------+')
def query():
	bad_words=['address','Email','Name and Section']
	for i in range(0,len(ques)):
		if not any(bad_words in ques[i] for bad_words in bad_words):
			query=ques[i]
			print('')
			query=query.replace(' ','+').replace('*','').replace(',' and '.' or '\'','').rstrip('+')
			stripped_query=query
			print(stripped_query,'\n')
			st_query.append(stripped_query)
			temp.write(stripped_query)
print(query())
print(len(ques)-len(st_query)," miscellaneous questions detected\ncontinuing.....\n")

def finalizing():
	for i in range(2,len(st_query)):
		if len(st_query)<len(ques):
			try:
				print('things going good.......\n')
				print('loading pages....\nsearching questions',st_query[i],'\n')
				gsearch.gsearch(st_query[i])
				webbrowser.open("https://google.com/search?q={0}".format(str(st_query[i])))
				top=raw_input("Open the top sites for the question itself??\n>> ")
				if top=='yes' or top=='y' or top=='Yes':
					webbrowser.open(gsearch.results[0]['link'] and gsearch.results[1]['link'] and gsearch.results[2]['link'])
					print('moving to next question...\n')
				else:
					print('moving to next question...\n')
			except KeyboardInterrupt:
				op=raw_input('exit , right ?? > ')
				if op=='yes' or op=='y' or op=='yeah':
					print("Okay,dude..")
					sys.exit(1)
				else:
					continue
finalizing()
print('# questions and results saved to {0} at {1}'.format(str(temp.name),str(tempfile.gettempdir())))