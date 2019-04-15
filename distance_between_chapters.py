#!/usr/bin/env/ python
import numpy as np

def reduced_latitude(lat):
    f = 1/298.257223563
    b = np.arctan((1 - f)*np.tan(lat))
    return b

# Lambert's formula,  https://en.wikipedia.org/wiki/Geographical_distance
def lambert(c1, c2, unit='m'):
    if c1[0] == c2[0] and c1[1] == c2[1]:
        return 0
    b1 = reduced_latitude(c1[0])
    b2 = reduced_latitude(c2[0])
    
    # Calculate centeral angle
    ca = np.arccos(np.sin(c1[1])*np.sin(c2[1]) 
                   + np.cos(c1[1])*np.cos(c2[1])*np.cos(c2[0] - c1[0]))

    P = (b1 + b2)/2
    Q = (b2 - b1)/2
    X = (ca - np.sin(ca))*np.sin(P)**2*np.cos(Q)**2/np.cos(ca/2)**2
    Y = (ca + np.sin(ca))*np.cos(P)**2*np.sin(Q)**2/np.sin(ca/2)**2
    a = 6378137 # meter
    f = 1/298.257223563
    d = a*(ca - f/2*(X + Y))

    # Unit conversion
    if unit == 'km':
        d *= 1e-3
    return d

chapters = []
ignore_list = ['Malmö',
               #'Lund',
               'Chalmers',
               #'Göteborg',
               #'KTH',
               'Stockholm',
               #'Luleå',
               'Karlstad',
               #'Uppsala',
               'Helsingborg',
               #'Linköping'
               ]

to_city = 'Göteborg'
destination = None

max_cost = 12500 # SEK


with open('Chapter_Coordinates.csv', 'r') as data_file:
    for line in data_file:
        if '#' in line:
            continue
        
        split = line.split(',')
        city = split[0]

        if any(ignore == city for ignore in ignore_list):
            print('Ignoring %s' % city )
            continue
        else:
            latitude = float(split[1])*np.pi/180
            longitude = float(split[2])*np.pi/180
            chapters.append([city, (longitude, latitude)])

for c in chapters:
    if c[0] == to_city:
        destination = c

if not destination:
    print('Could not find the destination "%s" in the the list of chapters!' % to_city)
    print('Exiting early!')
    exit()

distances = []
for c in chapters:
    d = lambert(c[1], destination[1], 'km')
    distances.append(d)
    print('Distance from {} to {} is {:.0f} km.'.format(c[0], destination[0], d))

max_d = max(distances)
sum_d = sum(distances)

longest_city_name = 0

for city in chapters:
    if len(city[0]) > longest_city_name:
        longest_city_name = len(city[0])


for d, c in zip(distances, [chap[0] for chap in chapters]):
    part_d = d/sum_d
    print('{:11}: {:>5.1f}% => {:>8.2f} SEK'.format(c, 100*part_d, max_cost*part_d))
