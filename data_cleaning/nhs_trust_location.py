import urllib2
import json
import csv


postcodes = []

seq = ['A', 'B', "C", "D", "E", "F", "G", "H", "I", "J", "K"]
codes = []

provider_postcode = {}

def getCodes():
    with open('/Users/Jake/Documents/Warwick/urss/data/diabetes/nati-diab-inp-audi-16-open-data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            codes.append(row['Provider Code'])

def readPostcodes():

    with open('/Users/Jake/Documents/Warwick/urss/data/other/nhs_trusts_england_info/etr.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=seq)
        for row in reader:
            if row['A'] in codes:
                postcodes.append(row['J'])
                provider_postcode[row['J']] = row['A']
                print row['A']
    with open('/Users/Jake/Documents/Warwick/urss/data/other/nhs_trusts_england_info/ets.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=seq)
        for row in reader:
            if row['A'] in codes:
                postcodes.append(row['J'])
                provider_postcode[row['J']] = row['A']
                print row['A']
    return

def writePostcodes(postcodes):
    with open('/Users/Jake/Documents/Warwick/urss/data/other/nhs_trusts_england_info/sites_loc.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|')
        for postcode in postcodes:
            writer.writerow([postcode['postcode'], postcode['lat'], postcode['lng'], postcode['code']])
    return

def getLonLat(postcodes):
    results = []

    def _getLongLat(postcode):
        formatted = postcode.replace(" ", "")
        try:
            response = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=" + formatted + "&sensor=true")
            data = json.load(response)
            results = data['results'][0]

            result = results['geometry']['location']
            result['postcode']=postcode
            result['code']=provider_postcode[postcode]
            print result
            return result

        except:
            error = ValueError("Could not find postcode:" + formatted)
            print error
            raise error

    for postcode in postcodes:
        try:
            results.append(_getLongLat(postcode))
        except:
            continue
    return results

getCodes()
readPostcodes()
result = getLonLat(postcodes)
print result
writePostcodes(result)
