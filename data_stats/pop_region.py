import pandas as pd
import csv

fileName = '/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/other/b-calculation-ccg-estmtd-reg/SNPP Projections-Table 1.csv'
regions = pd.read_csv('/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/other/ccg_map/Region-to-ccg.csv')

cols = ['2013', '2014', '2015', '2016', '2017']

def getRegionalStats(fileVal, col):
    print "**********"
    print "Regional Stats ", col
    data = pd.read_csv(fileName)

    def getCcgVal(ccg):
        val = data.loc[data['CCG'] == ccg]
        try:
            return val[col].iloc[0]
        except:
            return 0

    with open("/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/other/b-calculation-ccg-estmtd-reg/pop_region_" + str(fileVal) + ".csv", "wb") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|')
        for region in regions:
            print region
            tot = 0
            count = 0
            for row in regions[region]:
                if type(row) is str:
                    tot += getCcgVal(row)
                    count += 1
            mean = tot / count
            print "Total: ", tot
            writer.writerow([region, tot])


fileVal = 2013
for col in cols:
    #printStats(name)
    getRegionalStats(fileVal, col)
    fileVal += 1
