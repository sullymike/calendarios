import json
import html
import mysql.connector
from dateutil.parser import parse

from os.path import exists
import requests
from bs4 import BeautifulSoup

s = requests.Session()

r1 = s.get('https://www.hispashare.org/?')
soup = BeautifulSoup(r1.content, features="html.parser")


print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
soup1=soup.findAll('div', {"class": "WIN1_CONTAINER"})

print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
soup2=soup1.find_all('td')
for i in soup1.find_all('td'):
    print(i)
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')




w=1
for data in parsed_json:
    print(data)
    if (data.get('profesores') and data.get('codAsignatura') and data['codAsignatura'] != ''):
            #print(data)
            date1 = parse(data['start']).strftime('%s')
            date2 = parse(data['end']).strftime('%s')
            hours = (int(date2) - int(date1)) / 3600;
            query = 'SELECT id FROM clase WHERE Asignatura="' + html.unescape(data['title']) + '" AND codigo=' + str(
                data['codAsignatura']) + ' AND tipo="' + html.unescape(
                data['tipologia']) + '" AND start=' + date1 + ' AND grupo=' + data['grup'] + ' AND end=' + date2 + ' AND curse=' + str(
                curse) + ' AND yearaca=' + str(yearaca)

            mycursor.execute(query)
            myresult = mycursor.fetchall()
            if len(myresult) == 0:
                #print(w)
                query = 'INSERT INTO clase (Asignatura, codigo, tipo, start, end,hours,curse,grupo,grado,aula,yearaca) VALUES ("' + html.unescape(
                    data['title']) + '",' + str(data['codAsignatura']) + ',"' + html.unescape(
                    data['tipologia']) + '",' + date1 + ',' + date2 + ',' + str(hours) + ',' + str(curse) + ','+html.unescape(data['grup'])+ ','+str(i[0])+',"'+html.unescape(data['aula'])+ '",' + str(
                    yearaca) + ')'
                mycursor.execute(query)
                mydb.commit()
                #print(mycursor.rowcount, "record inserted.")
                idclase=mycursor.lastrowid
                if len(data['profesores']) > 1:
                    for profesor in data['profesores']:
                        idprofesor=profesordo(profesor)
                        query = 'INSERT INTO clases_profesor (clase, profesor) VALUES ('+str(idclase)+','+str(idprofesor)+')'
                        #print(query)
                        mycursor.execute(query)
                else:
                    if (data['profesores'][0] and html.unescape(data['profesores'][0]) != ''):
                        idprofesor=profesordo(profesor)
                        query = 'INSERT INTO clases_profesor (clase, profesor) VALUES ('+str(idclase)+','+str(idprofesor)+')'
                        mycursor.execute(query)
    w += 1