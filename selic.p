set title "SELIC"
set xdata time
set style data lines
set autoscale x
set autoscale y
set timefmt "%d/%m/%Y"
set xlabel "Data"
set ylabel "Valor"
set format x "%d\n%m\n%Y"
set term png
set output "selic.png"

plot "data.dat" using 1:2 t "Taxa SELIC" w linespoints, "plot.dat" u 1:3 w linespoints
