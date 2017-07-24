#script to format the stroke data
import csv

v2014 = {}
v2015 = {}
v2016 = {}
v2017 = {}

with open('/Users/Jake/Documents/Warwick/urss/data/stroke/ccg_data_unformatted_u60.csv', 'rU') as csvfile:
    reader = list(csv.reader(csvfile))
    ccg_row = reader[0]
    val_row = reader[1]
    cnt = 0
    n = 0
    for col in ccg_row:
        if cnt == 0:
            v2014[col] = val_row[n]
        if cnt == 1:
            v2015[col] = val_row[n]
        if cnt == 2:
            v2016[col] = val_row[n]
        if cnt == 3:
            v2017[col] = val_row[n]
        cnt = (cnt + 1) % 4
        n += 1

with open('/Users/Jake/Documents/Warwick/urss/data/stroke/ccg_data_u60.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|')
    for i in range(0, len(ccg_row), 4):
        col = ccg_row[i]
        writer.writerow([col, v2014[col], v2015[col], v2016[col], v2017[col]])



'''with open('/Users/Jake/Documents/Warwick/urss/data/other/nhs_trusts_england_info/etr.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=seq)
    for row in reader:
        if row['A'] in codes:
            postcodes.append(row['J'])
            provider_postcode[row['J']] = row['A']
            print row['A']'''
