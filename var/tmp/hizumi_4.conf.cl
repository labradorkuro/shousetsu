[program:hizumi_4_back]
command=sudo python /home/pi/hizumi_4.py
numprocs=1
redirect_stderr=true
stdout_logfile=/var/log/hizumi_4.log
user=root
