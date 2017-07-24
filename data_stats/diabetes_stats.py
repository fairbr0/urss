import pandas as pd
import csv
import operator

files = ['/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/diabetes/nati-diab-audi-rep1-eng-ccg-data-tab_2014-16_v2/2015-16 Type 2 other CP_TT-Table 1_mod.csv',
    '/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/diabetes/nati-diab-audi-rep1-eng-ccg-data-tab_2014-16_v2/2014-15 Type 2 other CP_TT-Table 1_mod.csv',
    '/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/diabetes/nati-diab-audi-rep1-eng-ccg-data-tab_2013-15/2013-14 Type 2 other CP_TT-Table 1_mod.csv',
    '/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/diabetes/nati-diab-audi-12-13-rep1-sup-ccg-lhb-dat-tab 2/cases-type2.csv'
        ]

names = pd.read_csv('/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/other/shapefiles/ccg_map/ccg_names.csv')
regions = pd.read_csv('/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/other/shapefiles/ccg_map/Region-to-ccg.csv')

healthiest_all = []
unhealthiest_all = []
def printStats(fileName):
    print "************"
    print fileName
    data = pd.read_csv(fileName)
    data = data[['practice', 'cases']]
    data = data.loc[data['practice'].str.len() == 3]

    data = pd.merge(data, names, on='practice', how='outer')

    print "mean: ", data['cases'].mean()
    print "std: ", data['cases'].std()
    print "**************"
    healthiest = data.sort_values(['cases'], ascending=[True])
    h = []
    for row in healthiest.head(10)['practice']:
        h.append(row)
    healthiest_all.append(h)
    unhealthiest = data.sort_values(['cases'], ascending=[False])
    h = []
    for row in unhealthiest.head(10)['practice']:
        h.append(row)
    unhealthiest_all.append(h)



def getRegionalStats(fileVal, fileName):
    print "**********"
    print "Regional Stats ", fileName
    data = pd.read_csv(fileName)
    data = data[['practice', 'cases']]
    data = data.loc[data['practice'].str.len() == 3]

    def getCcgVal(ccg):
        val = data.loc[data['practice'] == ccg]
        try:
            return val['cases'].iloc[0]
        except:
            return 0

    with open("/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/diabetes/diab_region_" + str(fileVal) + ".csv", "wb") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|')
        for col in regions:
            print col
            tot = 0
            count = 0
            for row in regions[col]:
                if type(row) is str:
                    tot += getCcgVal(row)
                    count += 1
            mean = tot / count
            print "Total: ", tot
            print "Mean: ", mean
            writer.writerow([col, tot, mean])

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
