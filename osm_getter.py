#script to get certain properties from osm for the UK
import urllib2

regions = {'north_manchester' : [-3.197,53.015,0.363,53.885],'south_east':[-2.395,50.310,1.527,51.283], 'south_west': [-5.878,49.930,-2.395,51.283],
    'london_midlands':[-3.076,51.283,1.648,52.133], 'bham_midlands':[-3.197,52.133,1.912,53.015], 'north_yorkshire':[-3.691,53.885,0.198,54.984],
    'north_northumberland':[-3.109,54.984,-1.219,55.829]}

tags = ['leisure=sports_centre', 'amenity=fast_food']

api_base = 'http://overpass.osm.rambler.ru/cgi/xapi_meta?'

def download(tag):
    for region in regions:
        print 'Downloading for ' + region
        bbox = ','.join(str(e) for e in regions[region])
        f = urllib2.urlopen(api_base + 'node[' + tag +'][bbox=' + bbox + ']')
        stag = tag.split("=")[1]
        lfile = open('/Users/Jake/Documents/Warwick/urss/data/other/' + stag + '_' + region + '.xml', 'wb')
        lfile.write(f.read())
        lfile.close()
    return

download(tags[0])
