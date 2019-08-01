#!/usr/bin/python3

import argparse
import csv
from pathlib import Path
import shutil
import os

parser = argparse.ArgumentParser()
parser.add_argument("readfolder", help='input folder')
args = parser.parse_args()

writefolder = '.'

def read_and_output_csv(readcsv, writecsv):
    with open(readcsv, newline='') as csvfile:
        irqreader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        dic = dict()
        for row in irqreader:
            for k, v in row.items():
                key = k.replace(',', '')
                if key in dic:
                    dic[key].append(v)
                else:
                    dic[key] = [v]
        initial = dict()
        for k, v in dic.items():
            try:
                initial[k] = float(v[0])
            except ValueError:
                initial[k] = 0.0
        maximum = dict()
        for k, v in dic.items():
            # convert to floats
            liste = []
            for vvv in v:
                try:
                    liste.append(float(vvv))
                except ValueError:
                    pass
            maximum[k] = float(max(liste))
        #print(maximum)
        rel = dict()
        num_entries = 0
        for k, v in dic.items():
            if k == 'timestamp_us':
                rel[k] = v
                num_entries = len(v)
                continue
            rel[k] = []
            for vv in v:
                try:
                    val = (float(vv) - initial[k]) / (maximum[k] - initial[k])
                except ValueError:
                    val = 0.0
                except TypeError:
                    val = 0.0
                except ZeroDivisionError:
                    val = 1.0
                rel[k].append(val)

        with open(writecsv, 'w+', newline='') as outfile:
            print(writecsv)
            writer = csv.DictWriter(outfile, delimiter=';', quotechar='"', fieldnames=rel.keys())
            writer.writeheader()
            for i in range(0, num_entries):
                rowdict = dict()
                for k, v in rel.items():
                    rowdict[k] = v[i]
                writer.writerow(rowdict)

irqfiles = Path(args.readfolder).glob('**/irq*-rate*.csv')
for fi in irqfiles:
    read_and_output_csv(str(fi), writefolder + '/' +  str(fi.stem) + '.csv')
