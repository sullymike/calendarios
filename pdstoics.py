from icalendar import Calendar, Event, vCalAddress, vText,vDatetime
from datetime import datetime
import pytz
import jsonmi
import os
import html

cal = Calendar()

cal.add('prodid', '-//Docencia Q-F Aplicada')
cal.add('version', '2.0')
cal.add('calscale', 'GREGORIAN')
cal.add('X-WR-TIMEZONE', 'Europe/Madrid')
cal.add('METHOD', 'PUBLISH')


with open('jorge.json', 'r') as fcc_file:
    fcc_data = json.load(fcc_file)

for eve in fcc_data:
   try:
        print(eve)
        event = Event()
        summary=html.unescape(eve['tipologia']) +" / "+ html.unescape(eve['title']).strip() +" ("+html.unescape(eve['aula']).strip()+")"
        event.add('summary', summary)
        #event.add('description',html.unescape(eve['tipologia']))

        datestart = datetime.strptime(eve['start'], "%Y-%m-%d %H:%M:%S")
        dateend = datetime.strptime(eve['end'], "%Y-%m-%d %H:%M:%S")
        event.add('dtstart', datetime(datestart.year, datestart.month, datestart.day, datestart.hour, datestart.minute,datestart.second, tzinfo=pytz.timezone('Europe/Madrid')))
        event.add('dtend',datetime(dateend.year, dateend.month, dateend.day, dateend.hour, dateend.minute, dateend.second,tzinfo=pytz.timezone('Europe/Madrid')))
        event.add('dtstamp', datetime(2022, 6, 1, 0, 0, 0,tzinfo=pytz.timezone('Europe/Madrid')))
        event.add('uid',eve['reseId'])
        cal.add_component(event)

   except:
        continue

print(cal)

f = open(os.path.join( 'example.ics'), 'wb')
f.write(cal.to_ical())
f.close()