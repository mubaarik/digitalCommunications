import subprocess
import re, sys

s = ""
for l in [0.0004, 0.0008, 0.0016, 0.0032, 0.0064, 0.0128, 0.0192, 0.0256, 0.0384, 0.0512, 0.06, 0.07, 0.08, 0.09, 0.1, 0.12, 0.13, 0.15, 0.16] :
   a=subprocess.Popen(['python', 'PS9.py' , '-n', '6', '-w' ,'16' ,'-l',str(l),'-t','10000'],stdout=subprocess.PIPE)
   out,err=a.communicate()

   observed_tput = float(out.split("\n")[1].split()[3])
   print l, observed_tput
   s += str(l) + " " + str(observed_tput) + "\n"

with open("sliding-data.dat", "w") as f:
   f.write(s)
print "Wrote data to file sliding-data.dat"
