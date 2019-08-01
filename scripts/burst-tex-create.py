#!/usr/bin/python3

import argparse
import csv
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfolder", help='input folder', default='..')
args = parser.parse_args()

measurement_folder = Path(args.inputfolder)
plot_folder = Path('.')
plot_folder.mkdir(parents=True, exist_ok=True)

begindoc=r"""\RequirePackage{luatex85}
\documentclass{standalone}
\usepackage{siunitx}
\usepackage{xcolor}
\usepackage{pgfplots}
\pgfplotsset{compat=newest}

\begin{document}%
  \definecolor{TUMBlue}           {cmyk}{1.00,0.43,0.00,0.00}% Pantone 300 C                                            
  \definecolor{TUMWhite}          {cmyk}{0.00,0.00,0.00,0.00}% White                                                    
  \definecolor{TUMBlack}          {cmyk}{0.00,0.00,0.00,1.00}% Black                                                    
  \definecolor{TUMDarkerBlue}     {cmyk}{1.00,0.54,0.04,0.19}% Pantone 301 C                                            
  \definecolor{TUMDarkBlue}       {cmyk}{1.00,0.57,0.12,0.70}% Pantone 540 C                                            
  \definecolor{TUMDarkGray}       {cmyk}{0.00,0.00,0.00,0.80}% 80% Black                                                
  \definecolor{TUMMediumGray}     {cmyk}{0.00,0.00,0.00,0.50}% 50% Black                                                
  \definecolor{TUMLightGray}      {cmyk}{0.00,0.00,0.00,0.20}% 20% Black                                                
  \definecolor{TUMIvony}          {cmyk}{0.03,0.04,0.14,0.08}% Pantone 7527 C                                           
  \definecolor{TUMOrange}         {cmyk}{0.00,0.65,0.95,0.00}% Pantone 158 C                                            
  \definecolor{TUMGreen}          {cmyk}{0.35,0.00,1.00,0.20}% Pantone 383 C                                            
  \definecolor{TUMLightBlue}      {cmyk}{0.42,0.09,0.00,0.00}% Pantone 283 C                                            
  \definecolor{TUMLighterBlue}    {cmyk}{0.65,0.19,0.01,0.04}% Pantone 542 C                                            
  \definecolor{TUMPurple}         {cmyk}{0.50,1.00,0.00,0.40}%                                                          
  \definecolor{TUMDarkPurple}     {cmyk}{1.00,1.00,0.00,0.40}%                                                          
  \definecolor{TUMTurquois}       {cmyk}{1.00,0.03,0.30,0.30}%                                                          
  \definecolor{TUMDarkGreen}      {cmyk}{1.00,0.00,1.00,0.20}%                                                          
  \definecolor{TUMDarkerGreen}    {cmyk}{0.60,0.00,1.00,0.20}%                                                          
  \definecolor{TUMYellow}         {cmyk}{0.00,0.10,1.00,0.00}%                                                          
  \definecolor{TUMDarkYellow}     {cmyk}{0.00,0.30,1.00,0.00}%                                                          
  \definecolor{TUMLightRed}       {cmyk}{0.00,0.80,1.00,0.10}%                                                          
  \definecolor{TUMRed}            {cmyk}{0.10,1.00,1.00,0.10}%                                                          
  \definecolor{TUMDarkRed}        {cmyk}{0.00,1.00,1.00,0.40}%                                                          
    \begin{tikzpicture}[>=latex]%                                                                                       
      \pgfplotscreateplotcyclelist{mystil}{%                                                                            
        {TUMBlue, mark=none},                                                                             
        {TUMOrange, mark=none},                                                                         
        {TUMGreen, mark=none},                                                                           
        {TUMBlue, densely dashed, mark=none},                                                                       
        {TUMOrange, densely dashed, mark=none},                                                                   
        {TUMGreen, densely dashed, mark=none}                                                                      
      }%

"""

beginaxis=r"""
		\begin{axis}[
		width=20cm,
		height=10cm,
		xmin=0,
		ymin=0,
		grid=major,
		xlabel = {Latency [\si{\micro\second}]},
		ylabel = {Packets},
		tick label style = {font=\scriptsize},
		cycle list name=mystil,
                legend pos = outer north east
		]
"""

endaxis=r"""		\end{axis}
"""

endtikzpic=r""" 	\end{tikzpicture}
"""

enddoc=r"""\end{document}

"""

addplot=r"""
                \addplot table[
			col sep=semicolon,
			x expr= \thisrowno{%s}/1000,
			y expr= \thisrowno{%s}/300000,
		]{%s};
                \addlegendentry{%s}
"""

# percentiles
#percentiles = sorted(list(measurement_folder.glob('**/*repeat0.pcap.percentiles.csv')), key=lambda x: (x.parent.name.split('-')[1], int(x.parent.name.split('-')[0][2:])))
stuff = sorted(list(measurement_folder.glob('*burst-latencies-pre*')), key=lambda x: int((x.name.split('-burst-')[0])))

bursts = set()
for s in stuff:
    burstsize = s.name.split('-burst-')[0]
    bursts.add(burstsize)
    liste = list(measurement_folder.glob('*latencies-pre-rate*-snort-filter.pcap.hist.csv'))
    rates = set()

    for l in liste:
        rate = l.name.split('rate')[1].split('-')[0]
        rates.add(rate)
    for rat in rates:
        with open(measurement_folder.joinpath(str(burstsize) + '-burst-latencies-pre-rate' + str(rat) + '-snort-filter.pcap.hist.csv')) as csvfl:
            reader = csv.DictReader(csvfl)
            agg = 0
            with open(str(burstsize) + '-burst-latencies-pre-rate' + str(rat) + '-snort-filter.pcap.cdf.csv', 'w', newline='') as csvwrtfl:
                writer = csv.DictWriter(csvwrtfl, fieldnames=['latency_bucket', 'count'], delimiter=';')
                for line in reader:
                    agg = agg + int(line['count'])
                    writer.writerow({'latency_bucket': line['latency_bucket'], 'count': agg})

bursts = sorted(bursts, key=lambda x: int(x))
for rat in rates:
    fhandle = open(str(plot_folder.joinpath('latencies-pre-rate' + str(rat) +'-snort-filter.tex')), 'w+')
    fhandle.write(begindoc)
    fhandle.write(beginaxis)
    for b in bursts:
        add = addplot % ('0', '1', str(b) + '-burst-latencies-pre-rate' + str(rat) + '-snort-filter.pcap.cdf.csv', 'burst' + str(b))
        fhandle.write(add)
    fhandle.write(endaxis)
    fhandle.write(endtikzpic)
    fhandle.write(enddoc)
