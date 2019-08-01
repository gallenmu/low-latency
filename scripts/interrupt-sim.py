import csv
import math
import subprocess

sec_in_ns = int(1 * 1000 * 1000 * 1000)

latex_compact = r"""\RequirePackage{luatex85}
\documentclass{standalone}
\usepackage{siunitx}
\usepackage{xcolor}
\usepackage{pgfplots}
\pgfplotsset{compat=newest}

\begin{document}
\definecolor{TUMOrange}{cmyk}{0.00,0.65,0.95,0.00}% Pantone 158 C
                \begin{tikzpicture}[>=latex]
                \pgfplotscreateplotcyclelist{mystil}{%
                {TUMOrange, fill=TUMOrange, mark=square*},
                }%
                \begin{axis}[
                width=15cm,
                height=10cm,
                ymin=0,
                grid=major,
                ylabel = {Latency [\si{\micro\second}]},
                xlabel = {Measurement time [\si{\second}]},
                tick label style = {font=\scriptsize},
                cycle list name = mystil,
                ]
                \addplot table[
                        col sep=semicolon,
                        scatter,
                        only marks,
                        x expr= \thisrowno{0}/1000000000,
                        y expr= \thisrowno{1}/1000,
                ]{"""

latex2 = r""".csv};
                \addlegendentry{simulation}
                \end{axis}
                \end{tikzpicture}
\end{document}
"""


def plot(hz, maxlen1, maxlen2, rate):
    inter_packet_gap = int(sec_in_ns / rate) # in nanoseconds
    interrupt_interval = sec_in_ns / hz

    low = interrupt_interval
    maxlen = maxlen1
    high = interrupt_interval + maxlen
    counter = 0

    with open(str('simulation.tex'), 'w', newline='\n') as texfile:
        #texfile.write(latex % args.path + str(rate) + latex2)
        texfile.write(latex_compact + str('simulation') + latex2)

    with open(str('simulation.csv'), 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        x = 0
        while x < sec_in_ns * 30:
            x += inter_packet_gap

            if x >= low and x <= high:
                delay = high - x
                spamwriter.writerow([x, delay])

            # new high low values
            if x >= high:
                low = low + interrupt_interval
                counter += 1
                if counter % 3 == 0:
                    maxlen = maxlen2
                else:
                    maxlen = maxlen1
                high = low + maxlen

hertz = 250
t = 0
while t < 1:
    rate = 10052 + t * 0.1
    plot(hertz, 10500, 15000, rate)
    #subprocess.call(['lualatex', 'simulation.tex'])
    t += 1

