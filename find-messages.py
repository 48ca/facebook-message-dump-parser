#!/usr/bin/python3

from bs4 import BeautifulSoup
from datetime import datetime
from sys import argv, exit
import IPython

if(len(argv) < 2):
    print("Specify an XML file to load")
    exit(1)

with open(argv[1], 'r') as f:
    data = f.read().replace('\n','')

print("Reading messages... this may take some time")
print("This will use approximately {0:2.2f} GB of memory...". format(4.04324283e-8 * len(data)))
soup = BeautifulSoup(data, 'html.parser')
print("Finding all messages...")
messages_prim = soup.find_all('div', {'class':'message'});
print("Found {} messages".format(len(messages_prim)))

print("Reading headers...")
headers = [{'id':i,'date':m.find("span",{'class':'meta'}).get_text()} for i,m in enumerate(messages_prim)]
print("Parsing dates...")
date_objects = [{'id':h['id'], 'date':datetime.strptime(h['date'],'%A, %B %d, %Y at %I:%M%p %Z')} for h in headers]
sorted_dates = sorted(date_objects, key=lambda x: x['date'])

print("Generating message objects...")
messages = [
    {
        'date': d['date'],
        'id': d['id'],
        'text': messages_prim[d['id']].find_next('p').get_text(),
        'user': messages_prim[d['id']].find('span', {'class': 'user'}).get_text()
    }
    for d in sorted_dates
]
print("Starting a shell:")
print(" > You can use the `messages` variable to access messages")
print(" > You may also use `soup` for the parsed XML and `headers` for the headers")
print(" > The messages straight from the XML are stored in `messages_prim`")
print(" > You can use the `format_messages()` function to print messages neatly")
print(" >>> format_messages() takes the start (and optionally end) chronological IDs for messages to be printed")
print(" > Because Facebook does not store the second at which a message was sent, messages sent during the same minute may be out of order")

# Pre-defined helper methods
def format_messages(s, e=0):
    if(s < 0): return
    ret = ""
    e = s+50 if e == 0 else max(e,s+1)
    for i in range(s, e):
        m = messages[i]
        ret += "({}) {} - {}: {}\n".format(
            m['id'],
            m['date'].strftime("%m/%d/%y %H:%M"),
            m['user'],
            m['text']
        )
    return ret[:-1] # Cut last '\n'

IPython.embed()

print("Cleaning up...")
