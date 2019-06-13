#Under Construction!
##Pipe Reports
####python version 2.7.5
####bash version 4.1.2(1)
####Purpose: Flag items acquired in the last 60 days to create a Newly Acquired flag for Primo
####Dependencies: the api scripts are using the socks and socket modules to place api calls via bela ; needs an analysis to retrieve in Analytics

---------------------------------------------------------

###get yesterday's pipe report with analytics api

input = config file with:

>url=https://api-na.hosted.exlibrisgroup.com/primo/v1/analytics/reports

>path=/shared/Primo Emory University/Reports/ACOOPE5/PipesReport

>apikey=[apikey]

>limit=1000

output = pipe delimited report

```
${bindir}primo_pipes_report_api.py ${config} > ${file} 2> $errorlog1
```
---------------------------------------------------------------

#####this can be used to parse the output file with bash

```
cat ${file}|while read line; do array=(`echo ${line} | sed 's/|/\n/g'`); echo ${array[1]}; done
```
