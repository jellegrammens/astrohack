import os
import sys
import csv
import argparse
import numpy as np
from datetime import datetime

from common import Galaxy
from ops import matrix

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input')
parser.add_argument('-a', '--arg', nargs='+', type=str)
args = parser.parse_args()
files = args.arg
input_dir = args.input

# t_start = datetime.now()
# print 'START {t}'.format(t=str(t_start))

train_dir = '/scratch/leuven/sys/ASTROHACK_DATA/{i}'.format(i=input_dir)
features = {}
first_ssid = None

for filename in files:
    galaxy = Galaxy()
    galaxy.ssid = filename.split('-g.csv')[0]
    first_ssid = first_ssid or galaxy.ssid
    print '{t}: processing {id}'.format(id=galaxy.ssid, t=str(datetime.now()))
    galaxy.matrix = np.loadtxt(os.path.join(train_dir, filename), delimiter=',')
    galaxy.isolate()
    galaxy.threed = matrix.reshape_to_3d_array(galaxy.isolated_matrix)
    galaxy.calculate_center()
    galaxy.calculate_sphericity()
    galaxy.find_local_maxima()
    features[galaxy.ssid] = (galaxy.sphericity, galaxy.flux, galaxy.volatility)
    # print galaxy.ssid, features[galaxy.ssid]

with open('/data/leuven/319/vsc31958/batched/{i}/features_{n}.csv'.format(n=first_ssid, i=input_dir), 'wb') as f:
    w = csv.writer(f)
    for feat, vals in features.iteritems():
        w.writerow((feat, ) + vals)

# print 'DONE {t}'.format(t=str(datetime.now()))
# print 'ELAPSED {t}'.format(t=str(datetime.now()-t_start))




