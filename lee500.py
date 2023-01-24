
filesin=('500_2020','500_2021','500_2022')
filesout=('los500_2020.txt','los500_2021.txt','los500_2022.txt')


fichero_datos="los500_2022.txt"
i=1
listadoT = {}



def readlinef(file):
    while True:
        line = f.readline()
        if not line:
            break
        if len(line) < 3:
            continue
        else:
            return line

j=0
for file in filesin:
    listado = {}
    i = 1
    with open(file) as f:
        while True:
            line = readlinef(f)
            line2 = readlinef(f)
            point=line.find(".")
            nsong=line[0:point]
            rest=line[point+1:]
            sing=rest.split("-")[0]
            album=rest.split("-")[1]
            #print(i,nsong,sing.strip(),album.strip(),line2.strip())
            listado[i]=sing.strip(),album.strip(),line2.strip()
            #line = f.readline(),[sing.strip(),album.strip(),line2.strip()]
            #print(f.readline())
            i += 1
            if i>500:
                break
            #i+=1


    fichero = open(filesout[j], mode='wt')
    fichero.write(str(listado))


    fichero.close()
    listadoT[j]=listado
    print(listadoT)
    j+=1