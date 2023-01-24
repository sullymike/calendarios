import requests
from bs4 import BeautifulSoup

s = requests.Session()

year='2021'
centro='104'

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


ht3='https://secretaria-virtual.uam.es/pds/consultaPublica/look[conpub]MostrarPubHora?rnd=9428.0'

ht2='https://secretaria-virtual.uam.es/pds/consultaPublica/[Ajax]selecionarRangoHorarios?rnd=350&start=0&end=2000000000'

for i in planes:
    for j in range(1, i[1] + 1):
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        plan = str(i[0])
        curso = str(j)
        data = {
            "planDocente": year,
            "centro": centro,
            "planEstudio": plan,
            "curso": curso,
            "trimestre": "-2/-2",
            "grupos": "111",
            "asignaturas": "16305",
            "idPestana": "1",
            "ultimoPlanDocente": "",
            "accesoSecretaria": "null"
        }
        ht1 = 'https://secretaria-virtual.uam.es/pds/consultaPublica/look[conpub]InicioPubHora?entradaPublica=true&idiomaPais=es.ES&planDocente=' + year + '&centro=' + centro + '&planEstudio=' + plan + '&curso=' + curso + '&trimestre=-2/-2&lock=false2'
        #print(ht1)
        r1 = s.get(ht1)
        soup = BeautifulSoup(r1.content, features="html.parser")
        try:
            grupos = soup.find('select', id="grupos")
            options = grupos.find_all("option")
            for option in options:
                # print(option.attrs.get('value'))
                data['grupo' + option.attrs.get('value')] = option.attrs.get('value')

            asignaturas = soup.find('select', id="asignaturas")
            options = asignaturas.find_all("option")
            data['asignaturas'] = options[0].attrs.get('value')
            for option in options:
                # print(option.attrs.get('value'))
                data['asignatura' + option.attrs.get('value')] = option.attrs.get('value')

            r = s.post(ht3, data)
            #print(data)
            cal = s.get(ht2).text
            fileopen=i[2].replace("/", "_") + "_" + str(j) + year+".cal"
            file = open(fileopen, 'w')
            file.write(cal)
            file.close()
            print(fileopen)

        except:
            print(fileopen)
            continue

