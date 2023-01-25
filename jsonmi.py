import json
import html
import mysql.connector
from dateutil.parser import parse
import requests
from bs4 import BeautifulSoup
from os.path import exists


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

def profesordo(profesor):
    profesor = html.unescape(profesor)
    query = 'SELECT id FROM profesor WHERE profesor="' + profesor + '"'
    mycursor.execute(query)
    myresultprof = mycursor.fetchall()
    # print(myresultprof)
    if len(myresultprof) == 0:
        print(profesor)
        dpto, proff = proffdpto(profesor)
        query = 'SELECT id FROM dpto WHERE dpto="' + dpto + '"'
        # print(query)
        mycursor.execute(query)
        myresultdpto = mycursor.fetchall()
        # print(myresultdpto)
        if len(myresultdpto) == 0:
            query = 'INSERT INTO dpto (dpto) VALUES ("' + dpto + '")'
            mycursor.execute(query)
            iddpto = mycursor.lastrowid
            queryprof = 'INSERT INTO profesor (profesor,email, dpto) VALUES("' + profesor + '","' + proff + '",' + str(
                iddpto) + ')'
            mycursor.execute(queryprof)
            idprofesor = mycursor.lastrowid
        else:
            iddpto = myresultdpto[0][0]
            queryprof = 'INSERT INTO profesor (profesor,email, dpto) VALUES("' + profesor + '","' + proff + '",' + str(
                iddpto) + ')'
            mycursor.execute(queryprof)
            idprofesor = mycursor.lastrowid
    else:
        idprofesor = myresultprof[0][0]

    return idprofesor,dpto

    query = 'INSERT INTO clases_profesor (clase, profesor) VALUES (' + str(idclase) + ',' + str(idprofesor) + ')'
    mycursor.execute(query)

planes=[[387,1,'Máster en Microbiología'],
[445,4,'Graduado/a en Biología'],
[446,4,'Graduado/a en Ciencias Ambientales'],
[448,4,'Graduado/a en Física'],
[449,4,'Graduado/a en Matemáticas'],
[477,1,'Máster en Ecología (2009)'],
[531,4,'Graduado/a en Bioquímica'],
[532,4,'Graduado/a en Nutrición Humana y Dietética'],
[547,1,'Máster en Biodiversidad'],
[551,1,'Máster en Genética y Biología Celular'],
[605,1,'Máster en Electroquímica. Ciencia y Tecnología'],
[619,1,'Máster en Ingeniería Química'],
[649,1,'Máster en Antropología Física: Evolución y Biodiversidad Humanas (2014)'],
[656,1,'Máster en Física de la Materia Condensada y de los Sistemas Biológicos'],
[672,4,'Graduado/a en Ciencias Ambientales y en Geografía y Ordenación del Territorio'],
[676,1,'Máster en Nanociencia y Nanotecnología Molecular (2015)'],
[678,1,'Máster en Biomoléculas y Dinámica Celular'],
[679,1,'Máster en Biotecnología (2015)'],
[688,1,'Máster en Matemáticas y Aplicaciones (2016)'],
[691,4,'Graduado/a en Química (2016)'],
[692,4,'Graduado/a en Ingeniería Química (2016)'],
[693,1,'Máster en Química Aplicada (2016)'],
[695,1,'Máster en Nuevos Alimentos'],
[696,1,'Máster en Ciencias Agroambientales y Agroalimentarias'],
[705,1,'Máster en Materiales Avanzados, Nanotecnología y Fotónica'],
[709,1,'Máster en Física Nuclear (2017)'],
[711,4,'Graduado/a en Ciencia y Tecnología de los Alimentos'],
[727,1,'Máster en Gestión Residuos y Aguas Residuales para la Recuperación de Recursos'],
[736,1,'Máster en Química Orgánica (2019)'],
[739,4,'Graduado/a en Nutrición Humana y Dietética y Ciencia y Tecnología de los Alimentos'],
[742,4,'Grado en Ciencias (UAB/UAM/UC3M)'],
[752,1,'Máster en Física Teórica (2020)'],
[761,1,'Máster en Energías y Combustibles para el Futuro (2021)'],
[762,1,'Máster en Química Teórica y Modelización Computacional (2021)'],
[764,1,'Máster en Biomedicina Molecular (2021)']]

#planes=[[691,4,'Graduado/a en Química (2016)']]
yearacaall=[2021]#2019,2020,2022

for yearaca in yearacaall:
    for i in planes:
        for j in range(1, i[1] + 1):
        #for j in range(2, 3):
            file=i[2].replace("/", "_") + "_" + str(j) + str(yearaca)+".cal"
            print(file)
            #file='Graduado_a en Biología_1.cal'
            if not exists(file):
                continue
            with open(file) as user_file:
                parsed_json = json.load(user_file)


            profesores=[]
            dpto=[]
            curse=j

            dbhost = 'localhost'
            dbname = 'PDS'
            dbuser = 'jorge'
            dbpasswd = 'XXXXXX'

            table_prefix = ''

            mydb = mysql.connector.connect(
              host=dbhost,
              user=dbuser,
              password=dbpasswd,
              database=dbname
            )
            mycursor = mydb.cursor()
            w=1
            for data in parsed_json:
                # print(data)
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
                                idprofesor,dpto=profesordo(profesor)
                                query = 'INSERT INTO clases_profesor (clase, profesor,dpto) VALUES ('+str(idclase)+','+str(idprofesor)+','+str(dpto)+')'
                                #print(query)
                                mycursor.execute(query)
                        else:
                            if (data['profesores'][0] and html.unescape(data['profesores'][0]) != ''):
                                idprofesor,dpto=profesordo(data['profesores'][0])
                                query = 'INSERT INTO clases_profesor (clase, profesor,dpto) VALUES ('+str(idclase)+','+str(idprofesor)+','+str(dpto)+')'
                                mycursor.execute(query)
                w += 1