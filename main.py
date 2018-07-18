from flask import Flask, request, jsonify
import requests
from flask_restful import Resource, Api
import boto3
import json
import datetime
import sys

app = Flask(__name__)
api = Api(app)

requestFile = ""
if 1 < len(sys.argv):
    requestFile=sys.argv[1]
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



class Events(Resource):
    def getevents():
        apikey = 'NTDAtQyt19LGVjiWyENJ9Mv5PAX9W7c4'
        u = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?"
            +"startDateTime="+startDate
            +"&postalcode="+postalcode
            +"&endDateTime="+endDate
            +"&city="+city
            +"&apikey="+apiKey)
        json_obj = u.text
        s3 = boto3.resource('s3')
        s3.Bucket('pyproj21').put_object(Key=str(time)+'/events.json',Body=json_obj)

        #print(json_obj)
    getevents()




api.add_resource(Events,'/get_events',methods=['GET'])
app.run(port=4535)
