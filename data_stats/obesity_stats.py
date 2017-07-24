import pandas as pd
import csv
import operator

files = ['/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/obesity/obes-phys-acti-diet-eng-2017-tab/obesity-england-2015:6.csv',
        '/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/obesity/obes-phys-acti-diet-eng-2016-tab/obesity-england-2014:5.csv',
        '/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/obesity/Obes-phys-acti-diet-eng-2015-tab/obesity-england-2013:4.csv'
        ]

names = pd.read_csv('/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/other/shapefiles/ccg_map/ccg_names.csv')
regions = pd.read_csv('/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/other/shapefiles/ccg_map/Region-to-ccg.csv')

healthiest_all = []
unhealthiest_all = []

def printStats(fileName):
    print "************"
    print fileName
    data = pd.read_csv(fileName, header=0)
    data = data.loc[(data['CCG'].str.len() == 3) & (data['CCG'].str[0] != 'Q')]

    print "mean: ", data['count'].mean()
    print "std: ", data['count'].std()
    print "**************"
    healthiest = data.sort_values(['count'], ascending=[True])
    h = []
    for row in healthiest.head(10)['CCG']:
        h.append(row)
    healthiest_all.append(h)
    unhealthiest = data.sort_values(['count'], ascending=[False])
    h = []
    for row in unhealthiest.head(10)['CCG']:
        h.append(row)
    unhealthiest_all.append(h)

def getRegionalStats(fileVal, fileName):
    print "**********"
    print "Regional Stats ", fileName

    data = pd.read_csv(fileName, header=0)
    data = data.loc[(data['CCG'].str.len() == 3) & (data['CCG'].str[0] != 'Q')]

    def getCcgVal(ccg):

        val = data.loc[data['CCG'] == ccg]
        try:
            return val['count'].iloc[0]
        except:
            return 0

    with open("/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/obesity/obesity_region_" + str(fileVal) + ".csv", "wb") as csvfile:
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
            print "Mean: ", mean
            writer.writerow([region, tot, mean])


def getCCGName(ccg):
    d = names.loc[names['practice'] == ccg]
    return d['name'].iloc[0]

def score(ccgs):
    scores = {}
    for col in ccgs:
        i = 10
        for row in col:
            if row in scores:
                scores[row] += i
            else:
                scores[row] = i
            i -= 1
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    named_scores = []
    for t in sorted_scores:
        name = getCCGName(t[0])
        tup = (name, t[1])
        named_scores.append(tup)
    print named_scores

for name in files:
    #printStats(name)
    printStats(name)

score(healthiest_all)
score(unhealthiest_all)
