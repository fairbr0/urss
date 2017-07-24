from string import ascii_uppercase
import csv
import re

counties = []

with open('counties.txt', 'rb') as f:
    for line in f:
        line = line.replace("\n", '')
        counties.append(line)

print counties
#o = open('towns.txt', 'wb')


def formatPlaces(c):
    f = open(c + '.txt', 'rb')
    for line in f:
        try:
            name = re.sub(r' - .*', "", line)
            name = name.replace('\n', '').lower()
            county = re.sub(r'.* - ', "", line)
            county = re.sub(r' .....N.*', "", county)
            county = county.replace("\n", '')
            if county not in counties:
                continue
            county = county.lower()
            lat = re.search(r'\d\d.\d\dN', line).group()[:5]
            obj = re.search(r'\d\d.\d\dW', line)
            if obj:
                lon = str(-1 * float(obj.group()[:5]))
            else:
                obje = re.search(r'\d\d.\d\dE', line)
                if obje:
                    lon = str(float(obje.group()[:5]))
                else:
                    lon = '00.00'
            line = name + ',' + county + ',' + lat + ',' + lon + '\n'
            o.write(line)
        except:
            print line
        #print line

def findOddPlaces(c):
    f = open(c + '.txt', 'rb')
    for line in f:
        try:
            obj = re.search(r'[^\s]+\d\d.\d\dN', line)
            if obj:
                name = re.sub(r'\d\d.\d\dN .*', "", line)
                county = name.replace('\n', '')
                name = county.lower()
                lat = re.search(r'\d\d.\d\dN', line).group()[:5]
                obj = re.search(r'\d\d.\d\dW', line)
                if obj:
                    lon = str(-1 * float(obj.group()[:5]))
                else:
                    obje = re.search(r'\d\d.\d\dE', line)
                    if obje:
                        lon = str(float(obje.group()[:5]))
                    else:
                        lon = '00.00'
                '''line = name + ',' + county.lower() + ',' + lat + ',' + lon + '\n'
                o.write(line)'''

                counties.append(county)
        except:
            print 'except', line

for c in ascii_uppercase:
    findOddPlaces(c)

#for c in ascii_uppercase:
#    formatPlaces(c)

with open('counties_.txt', 'wb') as f:
    for county in counties:
        f.write(county.lower()+'\n')
