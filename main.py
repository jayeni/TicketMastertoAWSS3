from flask import Flask, request, jsonify
import requests

import boto3
import json
import datetime
import sys

app = Flask(__name__)

#if 1 < len(sys.argv):
#    requestFile=sys.argv[1]




@app.route("/get_events",methods=['POST'])
def getevents():
    requestFile= request.form.get('file')
    def getJSON(fileName):
        with open(fileName, 'r') as f:
            return json.load(f)
    jObj= getJSON('./'+requestFile)

    time = datetime.datetime.utcnow()
    startDate = jObj.get("start_date_time","")
    endDate = jObj.get("end_date_time","")
    city  = jObj.get("city","")
    postalcode = jObj.get("postal_code","")
    apiKey = jObj.get("ticket_master_api_key","")
    u = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?"
        +"startDateTime="+startDate
        +"&postalcode="+postalcode
        +"&endDateTime="+endDate
        +"&city="+city
        +"&apikey="+apiKey)
    json_obj = u.text
    s3 = boto3.resource('s3')

    s3.Bucket('pyproj21').put_object(Key=str(time)+'/events.json',Body=json_obj)
    return 'SENT TO S3'
if __name__ == '__main__':
    app.run(port=8000)
