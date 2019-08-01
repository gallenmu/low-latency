#!/usr/bin/python3

from pathlib import Path
import re

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("measurement_folder", help='input folder', default='./results')
args = parser.parse_args()

measurement_folder = Path(args.measurement_folder)
plot_folder = Path('.')
plot_folder.mkdir(parents=True, exist_ok=True)

texheader=r"""\RequirePackage{luatex85}
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
        {TUMBlue, fill=TUMBlue, mark=none},
        {TUMOrange, fill=TUMOrange, mark=none},
        {TUMGreen, fill=TUMGreen, mark=none},
        {TUMBlue!30, fill=TUMBlue!30, mark=none},
        {TUMOrange!30, fill=TUMOrange!30, mark=none},
        {TUMGreen!30, fill=TUMGreen!30, mark=none}
      }%
"""
texheader2=r"""\RequirePackage{luatex85}
\documentclass{standalone}
\usepackage{siunitx}
\usepackage{xcolor}
\usepackage{pgfplots}
\pgfplotsset{compat=newest}

\begin{document}
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
        {TUMBlue, fill=TUMBlue, mark=*},
        {TUMOrange, fill=TUMOrange, mark=square*},
        {TUMGreen, fill=TUMGreen, mark=triangle*},
        {TUMBlue!30, fill=TUMBlue!30, mark=*},
        {TUMOrange!30, fill=TUMOrange!30, mark=square*},
        {TUMGreen!30, fill=TUMGreen!30, mark=triangle*}
      }%
"""
textableheader=r"""\RequirePackage{luatex85}
\documentclass{standalone}
\usepackage{siunitx}

\usepackage{booktabs}
\usepackage{csvsimple}

\begin{document}
    \begin{tabular}{lrrrrrrrrrrr}
    \toprule
    Name & Pre & Post & Rate &  Median & 90th percentile & 99th percentile & 99.9th percentile & 99.99th percentile & 99.999th percentile & 99.9999th percentile & Maximum\\
    \midrule
"""

textablefooter=r"""\end{tabular}
\end{document}
"""

texaxis=r"""
		\begin{axis}[
		width=15cm,
		height=10cm,
		xmin=0,
		ymin=0,
		xmax=1000,
		restrict x to domain=0:1000,
		grid=major,
		xlabel = {Latency [\si{\micro\second}]},
		ylabel = {Events},
		tick label style = {font=\scriptsize},
		point meta={y-x},
		ybar=0,
		cycle list name=mystil,
		bar width=.1pt
		]
"""

texaxisrestricted=r"""
		\begin{axis}[
		width=15cm,
		height=10cm,
		xmin=0,
		xmax=500,
		restrict x to domain=0:500,
		ymin=0,
		grid=major,
		xlabel = {Latency [\si{\micro\second}]},
		ylabel = {Events},
		tick label style = {font=\scriptsize},
		point meta={y-x},
		ybar=0,
		cycle list name=mystil,
		bar width=.1pt
		]
"""

texscatter=r"""
		\begin{axis}[
		width=15cm,
		height=10cm,
		ymin=0,
		grid=major,
		ylabel = {Latency [\si{\milli\second}]},
		xlabel = {Measurement time [\si{\second}]},
		tick label style = {font=\scriptsize},
		cycle list name=mystil
		]
"""


texfooter=r"""
		\end{axis}
		\end{tikzpicture}
\end{document}

"""

addplot=r"""
		\addplot table[%
			col sep=comma,
			x expr= \thisrowno{0}/1000,
			y expr= \thisrowno{1},
		]"""

addscatter=r"""
                \addplot table[%
			col sep=comma,
                        scatter,
                        only marks,
                        x expr= \thisrowno{1}/1000000000,
                        y expr= \thisrowno{0}/1000000,
                ]"""

ALL_TABLE_LINE = r"""%s&
                     \csvreader{%s}{}{\csvcoli}&
                     \csvreader{%s}{}{\csvcolii}&
                     \csvreader{%s}{}{\csvcoliii}&
                     \csvreader{%s}{}{\csvcoli}&
                     \csvreader{%s}{}{\csvcolii}&
                     \csvreader{%s}{}{\csvcoliii}&
                     \csvreader{%s}{}{\csvcoliv}&
                     \csvreader{%s}{}{\csvcolv}&
                     \csvreader{%s}{}{\csvcolvi}&
                     \csvreader{%s}{}{\csvcolvii}&
                     \csvreader{%s}{}{\csvcolviii}\\"""

# table of latency percentiles
fhandle = open(plot_folder.joinpath('all.tex'), 'w')
fhandle.write(textableheader)
percentiles = sorted(list(measurement_folder.glob('**/*.pcap.percentiles.csv')), key=lambda x: (x.name.split('-')[1], int(x.name.split('-')[2].replace('rate', '')) ))
for f in percentiles:
    filname = f.stem.replace('.pcap.percentiles', '')
    tf = str(f).replace('percentiles', 'transferrate')
    add = ALL_TABLE_LINE % (str(filname), tf, tf, tf, f, f, f, f, f, f, f, f)
    fhandle.write(add)
fhandle.write(textablefooter)

# table of latency percentiles-filtered (cut first second of measured data)
fhandle = open(plot_folder.joinpath('all-filtered.tex'), 'w')
fhandle.write(textableheader)
percentiles = sorted(list(measurement_folder.glob('**/*.pcap.percentiles-filtered.csv')), key=lambda x: (x.name.split('-')[1], int(x.name.split('-')[2].replace('rate', '')) ))
for f in percentiles:
    filname = f.stem.replace('.pcap.percentiles-filtered', '')
    tf = str(f).replace('percentiles-filtered', 'transferrate')
    add = ALL_TABLE_LINE % (str(filname), tf, tf, tf, f, f, f, f, f, f, f, f)
    fhandle.write(add)
fhandle.write(textablefooter)

# latency histogram
hist = sorted(list(measurement_folder.glob('**/*.pcap.hist.csv')))
for f in hist:
    filname = f.stem.replace('.hist', '')
    fhandle = open(plot_folder.joinpath(filname + '.hist.tex'), 'w')
    fhandle.write(texheader)
    fhandle.write(texaxis)
    add = "{%s};" % (str(f))
    fhandle.write(addplot + add)
    fhandle.write(texfooter)

# jitter histogram
jitterpre = sorted(list(measurement_folder.glob('**/*.pcap.jitterpre.csv')))
for f in jitterpre:
    filname = f.stem.replace('.jitterpre', '')
    fhandle = open(plot_folder.joinpath(filname + '.jitter.tex'), 'w')
    fhandle.write(texheader)
    fhandle.write(texaxisrestricted)
    add = "{%s};" % (str(f))
    fhandle.write(addplot + add)
    add = "{%s};" % (str(f).replace('jitterpre', 'jitterpost'))
    fhandle.write(addplot + add)
    fhandle.write(texfooter)

# worst of graph
worstof = sorted(list(measurement_folder.glob('**/*.pcap.worst.csv')))
for f in worstof:
    filname = f.stem.replace('.worst', '')
    fhandle = open(plot_folder.joinpath(filname + '.worst.tex'), 'w')
    fhandle.write(texheader2)
    fhandle.write(texscatter)
    add = "{%s};" % (str(f))
    fhandle.write(addscatter + add)
    fhandle.write(texfooter)

# worst-filtered of graph (cut first second of measured data)
worstof = sorted(list(measurement_folder.glob('**/*.pcap.worst-filtered.csv')))
for f in worstof:
    filname = f.stem.replace('.worst-filtered', '')
    fhandle = open(plot_folder.joinpath(filname + '.worst-filtered.tex'), 'w')
    fhandle.write(texheader2)
    fhandle.write(texscatter)
    add = "{%s};" % (str(f))
    fhandle.write(addscatter + add)
    fhandle.write(texfooter)

