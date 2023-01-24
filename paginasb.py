import json
import html
import mysql.connector
from dateutil.parser import parse
import requests
from bs4 import BeautifulSoup

profesros=['Jesus Lemus Torres','Maria Ines Alonso Montero','Ana Isabel Ruiz Garcia','Francisco Heras Muñoz','Alfredo Aguado Gomez','Jaime Fernando Cuevas Rodriguez','Maria Mercedes Rodriguez Fernandez','Manuel Chicharro Santamaria','Paula Mori Sanchez','Isidro de Pablo Lopez','J. Carlos Rodriguez Ubis','Luis Mendez Ambrosio','Alicia Palacios Cañas','Laia Domingo Colomer','Marco Antonio Jiménez González','Emiliano Martinez Periñan','Maria Lourdes Hernandez Apaolaza','Jose Julian Aleman Lara','Sergio Diaz-Tendero Victoria','Carmen Belen Molina Caballero']

def proffdpto(profesor):
    url = 'https://autoservicio.uam.es/paginas-blancas/buscarPersonas.do;jsessionid=bLz9vyLMR1jj6vL6VCpr06jGfJfFTqN4Lq6F4w6rdHX9YBpX1h2S!803235174';
    data = {'nombreFiltro': profesor.encode('ISO-8859-15'),
            'buscar': ''}  # 'nombreFiltro=Valle Lazaro, Juan Carlos del&buscar

    s = requests.Session()
    r = s.post(url, data)
    soup = BeautifulSoup(r.content, features="html.parser")

    #print(soup.text)

    dptop = soup.text.find('Departamento/U.O.:')
    centrop = soup.text.find('Centro/U.O.:')
    correop = soup.text.find('Correo Electrónico:')
    otrap = soup.text.find('otra búsqueda')
    if dptop>0:
        dpto=soup.text[dptop + 20:centrop].strip()
    else:
        dpto='Falta'
    if dptop>0 and correop>0:
        correo=soup.text[correop + 20:otrap].strip()
    else:
        correo='Falta'

    return dpto, correo

#print(proffdpto('Francisco Heras Muñoz'.encode('ISO-8859-15')))
for profesor in profesros:
    print(profesor,proffdpto(profesor))