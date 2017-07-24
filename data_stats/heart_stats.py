import pandas as pd
import operator

files = ['/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/heart_disease/cvd-local-mortality-statistics--maps-201012/by LA-Table 1_mod.csv',
    '/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/heart_disease/cvd_stats_2017_chapter1_mortality/1.19-Table 1_mod.csv'
    ]

names = pd.read_csv('/Users/Jake/Library/Mobile Documents/com~apple~CloudDocs/Warwick/urss/data/other/shapefiles/ccg_map/ccg_names.csv')

healthiest_all = []
unhealthiest_all = []

def printStats(fileName):
    print "************"
    print fileName
    data = pd.read_csv(fileName, header=0)
    data = data.loc[data['Code'].str.len() == 4]

    print "mean: ", data['Total 100000'].mean()
    print "std: ", data['Total 100000'].std()
    print "**************"
    healthiest = data.sort_values(['Total 100000'], ascending=[True])
    h = []
    for row in healthiest.head(10)['Name']:
        h.append(row)
    healthiest_all.append(h)
    unhealthiest = data.sort_values(['Total 100000'], ascending=[False])
    h = []
    for row in unhealthiest.head(10)['Name']:
        h.append(row)
    unhealthiest_all.append(h)


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
    print sorted_scores

for name in files:
    #printStats(name)
    printStats(name)

score(healthiest_all)
score(unhealthiest_all)
