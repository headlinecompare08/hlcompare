from bs4 import BeautifulSoup
import requests
#scrapes headlines and links and puts to format easy to add to database
#creates list of lists in format (newspaperid, headlinerank, headline, headlinelink)
#soup
url = 'https://nytimes.com'
nytimes_content = requests.get(url)
nytimes_soup = BeautifulSoup(nytimes_content.content,"html.parser")
nytimes_headlines = BeautifulSoup(nytimes_content.content,"html.parser").findAll("h2"
)


#numbered list with headlines

dailyrank = 1
nytimeslist = []
for v in nytimes_headlines:
  if "css-km70tz" not in str(v):
    if "css-9wqu2x" not in str(v):
      if v.text != "Site Index":
        if v.text != "Site Information Navigation":
          
          interlist = [1]
          interlist.append(dailyrank)
          dailyrank += 1
          interlist.append(v.text)
          nytimeslist.append(interlist)
  
#list of urls in same order as headline list
hreflist = []

for v in nytimes_soup.find_all('a', href=True):
  if "<h2" in str(v):
    if "css-km70tz" not in str(v):
      hreflist.append(v['href'])

  
  

  
#correct links that shortcut root page
hreflist2 = []
for i in hreflist:
  if "https:" in i:
    hreflist2.append(i)
  else:
    hreflist2.append("https://nytimes.com" + i)
#add dailyrank numbers to links so can match with headline list

hreflistfinal = []
dailyrank2 = 1
for i in hreflist2:
  interlist3 = []
  interlist3.append(dailyrank2)
  dailyrank2 += 1
  interlist3.append(i)
  hreflistfinal.append(interlist3)

#join headline list and final link list
counter4 = 0
for i in hreflistfinal:
    for y in nytimeslist:
      if i[0] == y[1]:
        nytimeslist[counter4].append(i[1])
        counter4 += 1
#data is in nytimeslist




#soup it up
url = 'https://foxnews.com'
fn_content = requests.get(url)
fn_soup = BeautifulSoup(fn_content.content,"html.parser")
fn_main = fn_soup.find_all("main")
main = str(fn_main)
main_soup = BeautifulSoup(main, "html.parser")
main_h2 = main_soup.find_all("h2")




#create numbered list of headlines
counter = 0
dailyrank = 1
fnlist = []
for v in main_h2:
  
 
  interlist = [3]
  interlist.append(dailyrank)
  dailyrank += 1
  interlist.append(v.text.lstrip().rstrip())
  fnlist.append(interlist)
  

#extract urls part 1 -> cut off leading
h2_html = []
counter1 = 0
for v in main_h2:
  if "https" in str(v):
    h2_html.append(str(v)[27:])
  else:
    h2_html.append(str(v)[29:])
  counter1 += 1

#extract urls part 2: find index of where to cut off trailing
link_end = []

for i in h2_html:
  link_end.append(str(i).index('>'))


#actually cut off trailing
link_rip = []
link_end_index = 0

for i in h2_html:
  a = link_end[link_end_index]
  link_rip.append(i[:a])
  link_end_index +=1

#combine headline list with urls
link_rip_index = 0
for i in fnlist:
  b = link_rip[link_rip_index]
  i.append(b)
  link_rip_index += 1
#final in fnlist

url = 'https://bbc.com'
bbc_content = requests.get(url)
bbc_soup = BeautifulSoup(bbc_content.content,"html.parser")
bbc_headlines = bbc_soup.findAll("h3", {"class":"media__title"})
counter = 0 
dailyrank = 1
bbclist = []
for v in bbc_headlines:
  
  interlist = [2]
  interlist.append(dailyrank)
  dailyrank += 1
  interlist.append(v.text.lstrip().rstrip())
  bbclist.append(interlist)  


bbc_hrefs_soup = bbc_soup.findAll("a", {"class":"media__link"})

hrefs = []

for v in bbc_hrefs_soup:
  if "https:" in v["href"]:
    hrefs.append(v['href'])
  else:
    hrefs.append("https://bbc.com" + v['href'])


dailyrank2 = 1
hrefsfinal = []
dailyrank2 = 1
for i in hrefs:
  interlist3 = []
  interlist3.append(dailyrank2)
  dailyrank2 += 1
  interlist3.append(i)
  hrefsfinal.append(interlist3)

counter4 = 0
for i in hrefsfinal:
    for y in bbclist:
      if i[0] == y[1]:
        bbclist[counter4].append(i[1])
        counter4 += 1
#final in bbclist

from django.utils import timezone

from models import Headline

for i in nytimeslist:
    nytimes = Headline(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1])
    nytimes.save()

for i in fnlist:
    foxnews = Headline(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1])
    foxnews.save()

for i in bbclist:
    bbc = Headline(headline=i[2], newspaper=i[0],link=i[3], day_order=i[1])
    bbc.save()
