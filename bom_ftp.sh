#!/bin/bash

cd /home/pi/epaper/weatherdata
DATE=`date -I`
echo $DATE

curl -O -u anonymous: ftp://ftp.bom.gov.au/anon/gen/fwo/IDV17300.txt

/usr/bin/grep -i Melbourne -A 3 IDV17300.txt > todays_weather.txt

/usr/bin/awk '{if (NR==2) {print}}' todays_weather.txt > weather_$DATE.txt
/usr/bin/awk '/Max/ { print $NF }' todays_weather.txt >> weather_$DATE.txt

cd ..

python3 epaper-refresh.py

exit 0
