#!/usr/bin/python3

from pathlib import Path

import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("histogram", help='input histogram folder')
args = parser.parse_args()

histogram = Path(args.histogram)
plot_folder = Path('.')
#plot_folder.mkdir(parents=True, exist_ok=True)

histograms = list(histogram.glob('**/*.pcap.hist.csv'))
for hist in histograms:

    filname = hist.stem.replace('.hist', '.hist.cdf')
    #print(filname)

    with open(hist, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader)
        total = 0
        for row in spamreader:
            total += int(row[1])

    with open(hist, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader)
        with open(plot_folder.joinpath(filname + '.csv'), 'w', newline='') as csvfile:
            
	    spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            integrator = 0
            for row in spamreader:
                integrator += int(row[1])
                if (1 - (float(integrator)/total)) > 0.0:
                    magic = 1 / (1 - float(integrator)/total)
                    spamwriter.writerow([str(row[0]), str(magic), str(integrator), str('{:.20f}'.format(float(integrator)/total))])

# table of latency percentiles
#fhandle = open(plot_folder.joinpath('all.tex'), 'w')
#handle.write(textableheader)
#percentiles = sorted(list(measurement_folder.glob('**/*.pcap.percentiles.csv')), key=lambda x: (x.name.split('-')[1], int(x.name.split('-')[2].replace('rate', '')) ))
#for f in percentiles:
#    filname = f.stem.replace('.pcap.percentiles', '')
#    tf = str(f).replace('percentiles', 'transferrate')
#    add = ALL_TABLE_LINE % (str(filname), tf, tf, tf, f, f, f, f, f, f, f, f)
#    fhandle.write(add)
#fhandle.write(textablefooter)
