import re
import requests 
from bs4 import BeautifulSoup 
import codecs
  
#URL = "https://www.canadavisa.com/express-entry-invitations-to-apply-issued.html#gs.ag3ms2"
URL = "https://meduza.io/rss/all"
r = requests.get(URL) 

encodedText = r.text.encode("utf-8")
soup = BeautifulSoup(encodedText)
text =  str(soup.findAll('description'))
print(text)