import json
import csv
import requests
covidurl = "https://covidtracking.com/api/v1/states/daily.json"
popurl = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/state/detail/SCPRC-EST2019-18+POP-RES.csv"

days = 50 * 14
avgpos = 0
cumtot = 0
tgtpermo = 45 / 1000 # This is a per month number

rpop = requests.get(popurl)
poptext = rpop.content.decode('utf-8')
popcsv = csv.reader(poptext.splitlines(), delimiter=",")
for row in popcsv:
    if row[4] == 'Virginia':
        testtgt = tgtpermo * int(row[5]) * 14 / 30
        break

rcovid = requests.get(covidurl)
covidjson = json.loads(rcovid.text)
for i in range(0, days):
    VA = covidjson[i]
    if VA['state'] == 'VA':
        pos = VA['positiveIncrease']
        tot = VA['totalTestResultsIncrease']
        
        avgpos = avgpos + pos
        cumtot = cumtot + tot
        
        print("Current positive rate as of {dte} is {pcnt:.2%} and total tests were {tot:,}".format(dte = VA['date'], pcnt = pos / tot, tot = tot))

print("The 14-day avg positive rate is {pcnt:.2%} and total tests were {tot:,}".format(dte = VA['date'], pcnt = avgpos / cumtot, tot = cumtot))

print("Target testing is {tgt:,}".format(tgt = testtgt))
