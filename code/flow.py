import os
import sys
import csv
import argparse
import numpy as np
from datetime import datetime

from common import Galaxy
from ops import matrix


#gdir = '/Users/elissamatton/astro/AstroData/Sample2/Sample_Data/SAMPLE/'

parser = argparse.ArgumentParser()
parser.add_argument('--mode', default='sample')
args = parser.parse_args()

astro_dir = '/scratch/leuven/sys/ASTROHACK_DATA'
sample_suff = 'Sample_Data/SAMPLE'
train_suff = 'Train'
if args.mode == 'debug':
    data_dir = '/data/leuven/319/vsc31958/debug'
else:
    data_dir = os.path.join(astro_dir, train_suff if args.mode == 'train' else sample_suff)
print 'parsing {d}'.format(d=data_dir)
features = {}

t_start = datetime.now()
print 'START {t}'.format(t=str(t_start))

files = [f for f in os.listdir(data_dir) if f.endswith("-g.csv")]
n = len(files)
c = 0
for filename in files:
    c += 1
    galaxy = Galaxy()
    galaxy.ssid = filename.split('-g.csv')[0]
    print 'processing {i}/{n}: {id}'.format(id=galaxy.ssid, i=c, n=n)
    galaxy.matrix = np.loadtxt(os.path.join(data_dir, filename), delimiter=',')
    galaxy.isolate()
    galaxy.threed = matrix.reshape_to_3d_array(galaxy.isolated_matrix)
    galaxy.calculate_center()
    galaxy.calculate_sphericity()
    galaxy.find_local_maxima()
    features[galaxy.ssid] = (galaxy.sphericity, galaxy.flux, galaxy.volatility)
    print galaxy.ssid, features[galaxy.ssid]

with open('/user/leuven/319/vsc31958/code/results/features_{n}.csv'.format(n=args.mode), 'wb') as f:
    w = csv.writer(f)
    for feat, vals in features.iteritems():
        w.writerow((feat, ) + vals)

print 'DONE {t}'.format(t=str(datetime.now()))
print 'ELAPSED {t}'.format(t=str(datetime.now()-t_start))




