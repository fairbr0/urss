import pandas as pd
import csv
import operator

fileName = '/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/stroke/ccg_data_u60.csv'
cols = ['cases14', 'cases15', 'cases16', 'cases17']
names = pd.read_csv('/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/other/shapefiles/ccg_map/ccg_names.csv')
regions = pd.read_csv('/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/other/shapefiles/ccg_map/Region-to-ccg.csv')

healthiest_all = []
unhealthiest_all = []

def printStats(col):
    print "************"
    print col
    data = pd.read_csv(fileName, header=0)
    data = data.loc[data['practice'].str.len() == 3]

    data = pd.merge(data, names, on='practice', how='outer')

    print "mean: ", data[col].mean()
    print "std: ", data[col].std()
    print "**************"
    healthiest = data.sort_values([col], ascending=[True])
    h = []
    for row in healthiest.head(10)['practice']:
        h.append(row)
    healthiest_all.append(h)
    unhealthiest = data.sort_values([col], ascending=[False])
    h = []
    for row in unhealthiest.head(10)['practice']:
        h.append(row)
    unhealthiest_all.append(h)

def getRegionalStats(fileVal, col):
    print "**********"
    print "Regional Stats ", col

    data = pd.read_csv(fileName, header=0)
    data = data.loc[data['practice'].str.len() == 3]

    def getCcgVal(ccg):

        val = data.loc[data['practice'] == ccg]
        try:
            return val[col].iloc[0]
        except:
            return 0

    with open("/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/stroke/stroke_region_" + str(fileVal) + "_u60.csv", "wb") as csvfile:
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

fileVal = 2017
for col in cols:
    getRegionalStats(fileVal, col)
    fileVal -= 1

#score(healthiest_all)
#score(unhealthiest_all)
