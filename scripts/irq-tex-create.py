#!/usr/bin/python3

import argparse
import csv
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputfolder", help='input folder', default='./irq-results')
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
	% TUM primary colors
	\definecolor{TUMBlue}		{cmyk}{1.00,0.43,0.00,0.00}	% Pantone 300 C
	\definecolor{TUMWhite}		{cmyk}{0.00,0.00,0.00,0.00}	% White
	\definecolor{TUMBlack}		{cmyk}{0.00,0.00,0.00,1.00}	% Black
%
	% TUM secondary colors (can be used with 100%, 80%, 50% and 20%)
	\definecolor{TUMDarkerBlue}	{cmyk}{1.00,0.54,0.04,0.19}	% Pantone 301 C
	\definecolor{TUMDarkBlue}	{cmyk}{1.00,0.57,0.12,0.70}	% Pantone 540 C
%
	\definecolor{TUMDarkGray}	{cmyk}{0.00,0.00,0.00,0.80}	% 80% Black
	\definecolor{TUMMediumGray}	{cmyk}{0.00,0.00,0.00,0.50}	% 50% Black
	\definecolor{TUMLightGray}	{cmyk}{0.00,0.00,0.00,0.20}	% 20% Black
%
	% TUM highlight colors
	\definecolor{TUMIvony}		{cmyk}{0.03,0.04,0.14,0.08}	% Pantone 7527 C
	\definecolor{TUMOrange}		{cmyk}{0.00,0.65,0.95,0.00}	% Pantone 158 C
	\definecolor{TUMGreen}		{cmyk}{0.35,0.00,1.00,0.20}	% Pantone 383 C
	\definecolor{TUMLightBlue}	{cmyk}{0.42,0.09,0.00,0.00}	% Pantone 283 C
	\definecolor{TUMLighterBlue}	{cmyk}{0.65,0.19,0.01,0.04}	% Pantone 542 C
%
	% Additional TUM diagram colors
	\definecolor{TUMPurple}		{cmyk}{0.50,1.00,0.00,0.40}
	\definecolor{TUMDarkPurple}	{cmyk}{1.00,1.00,0.00,0.40}
	\definecolor{TUMTurquois}	{cmyk}{1.00,0.03,0.30,0.30}
	\definecolor{TUMDarkGreen}	{cmyk}{1.00,0.00,1.00,0.20}
	\definecolor{TUMDarkerGreen}	{cmyk}{0.60,0.00,1.00,0.20}
	\definecolor{TUMYellow}		{cmyk}{0.00,0.10,1.00,0.00}
	\definecolor{TUMDarkYellow}	{cmyk}{0.00,0.30,1.00,0.00}
	\definecolor{TUMLightRed}	{cmyk}{0.00,0.80,1.00,0.10}
	\definecolor{TUMRed}		{cmyk}{0.10,1.00,1.00,0.10}
	\definecolor{TUMDarkRed}	{cmyk}{0.00,1.00,1.00,0.40}
%
	\pgfplotscreateplotcyclelist{mystil}{%
		{TUMBlue, mark=none},
		{TUMDarkerBlue, mark=none},
		{TUMOrange, mark=none},
		{TUMGreen, mark=none},
		{TUMPurple, mark=none},
		{TUMDarkPurple, mark=none},
		{TUMTurquois, mark=none},
		{TUMDarkYellow, mark=none},
		{TUMMediumGray, mark=none},
		{TUMRed, mark=none},
		{TUMBlue!50, mark=none},
		{TUMDarkerBlue!50, mark=none},
		{TUMOrange!50, mark=none},
		{TUMGreen!50, mark=none},
		{TUMPurple!50, mark=none},
		{TUMDarkPurple!50, mark=none},
		{TUMTurquois!50, mark=none},
		{TUMDarkYellow!50, mark=none},
		{TUMMediumGray!50, mark=none},
		{TUMRed!50, mark=none},
		{TUMBlue, densely dashed, mark=none},
		{TUMDarkerBlue, densely dashed, mark=none},
		{TUMOrange, densely dashed, mark=none},
		{TUMGreen, densely dashed, mark=none},
		{TUMPurple, densely dashed, mark=none},
		{TUMDarkPurple, densely dashed, mark=none},
		{TUMTurquois, densely dashed, mark=none},
		{TUMDarkYellow, densely dashed, mark=none},
		{TUMMediumGray, densely dashed, mark=none},
		{TUMRed, densely dashed, mark=none},
		{TUMBlue!50, densely dashed, mark=none},
		{TUMDarkerBlue!50, densely dashed, mark=none},
		{TUMOrange!50, densely dashed, mark=none},
		{TUMGreen!50, densely dashed, mark=none},
		{TUMPurple!50, densely dashed, mark=none},
		{TUMDarkPurple!50, densely dashed, mark=none},
		{TUMTurquois!50, densely dashed, mark=none},
		{TUMDarkYellow!50, densely dashed, mark=none},
		{TUMMediumGray!50, densely dashed, mark=none},
		{TUMRed!50, densely dashed, mark=none},
	        {TUMBlue, densely dotted, mark=none},
		{TUMDarkerBlue, densely dotted, mark=none},
		{TUMOrange, densely dotted, mark=none},
		{TUMGreen, densely dotted, mark=none},
		{TUMPurple, densely dotted, mark=none},
		{TUMDarkPurple, densely dotted, mark=none},
		{TUMTurquois, densely dotted, mark=none},
		{TUMDarkYellow, densely dotted, mark=none},
		{TUMMediumGray, densely dotted, mark=none},
		{TUMRed, densely dotted, mark=none},
		{TUMBlue!50, densely dotted, mark=none},
		{TUMDarkerBlue!50, densely dotted, mark=none},
		{TUMOrange!50, densely dotted, mark=none},
		{TUMGreen!50, densely dotted, mark=none},
		{TUMPurple!50, densely dotted, mark=none},
		{TUMDarkPurple!50, densely dotted, mark=none},
		{TUMTurquois!50, densely dotted, mark=none},
		{TUMDarkYellow!50, densely dotted, mark=none},
		{TUMMediumGray!50, densely dotted, mark=none},
		{TUMRed!50, densely dotted, mark=none}
	}
"""

begintikzpic=r"""   \begin{tikzpicture}[>=latex]%
"""

beginaxis=r"""                \begin{axis}[%
		width=20cm,
		height=10cm,
		xmin=0,
		ymin=0,
		grid=major,
		xlabel = {Measurement time [\si{\second}]},
		ylabel = {IRQ [relative]},
		tick label style = {font=\scriptsize},
		cycle list name=mystil,
                legend pos = outer north east
		]%
"""

endaxis=r"""		\end{axis}%
"""

endtikzpic=r""" \end{tikzpicture}%
"""

enddoc=r"""\end{document}

"""

addplot=r"""                \addplot table[
			col sep=semicolon,
			x expr= \thisrowno{%s}/1000000,
			y expr= \thisrowno{%s},
		]{%s};
                \addlegendentry{%s}
"""

def filter_cpunum(liste):
    cpu = set()
    for haeufle in liste:
        el = haeufle.split('_')
        c = el[len(el) - 1]
        if re.match('CPU\d+', c):
            cpu.add(c)
    return sorted(list(cpu))

# percentiles
stuff = sorted(list(measurement_folder.glob('**/irq*.csv')), key=lambda x: int((x.name.split('-')[1].replace('rate', ''))))
for f in stuff:
    fhandle = open(str(plot_folder.joinpath(str(f.stem) + '.tex')), 'w+')
    fhandle.write(begindoc)
    with open(str(f), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        header = list(next(reader, None))

        cpu_list = filter_cpunum(header)
        timestamp_index = header.index('timestamp_us')

        for cnum in cpu_list:
            fhandle.write(begintikzpic)
            fhandle.write(beginaxis)
            plotlist = []
            for i in header:
                if i == 'timestamp_us' or cnum not in i:
                    continue
                else:
                    plotlist.append([timestamp_index, header.index(i), str(f), i.replace('_', '\\_')])
            plotlist.sort(key=lambda x: x[3])
            for pl in plotlist:
                add = addplot % (pl[0], pl[1], pl[2], pl[3])
                fhandle.write(add)
            fhandle.write(endaxis)
            fhandle.write(endtikzpic)

    fhandle.write(enddoc)
