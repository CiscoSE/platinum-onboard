import configparser
import teamsapi
from utilities import print_details
from flask import Flask,jsonify,request
import db

# This flag turns on debugging of the web messages hitting the flask server
WEBDEBUG=True

print ("Platinum Onboard Engine Starting...\n")

app = Flask(__name__)

# Open up the configuration file and get all application defaults

config = configparser.ConfigParser()

try:
    config.read('package_config.ini')
except configparser.Error:
    print("Error: Unable to open package_config.ini")
    exit(-1)

try:
    teamsurl = config.get("platinum-onboard","url")
except ConfigParser.NoOptionError:
    # Defaulting to the standard Spark API
    teamsurl = "https://api.ciscospark.com"

try:
    teamstoken = config.get("platinum-onboard","token")
    module2ip = config.get("platinum-onboard","security-ip")
except:
    print("Error: Required items are not present in the configuration file.")
    exit(-1)

#
# Initialize the connection to the database
#
ret = db.initialize_database("platinum-onboard.db")
if ret == False:
    print ("Error: Unable to initialize the database.")
    exit(-1)

#
# Main Program Logic
#

# Route Point for generic message when web server is hit.
@app.route('/')
def index():
    if WEBDEBUG:
        print_details(request)
    return "Welcome to the Platinum Onboard Engine...\n"

# Returns a json representing the state of the application server
@app.route('/health')
def apphealth():
    if WEBDEBUG:
        print_details(request)
    return jsonify({"health":"running"})

# Returns a json representing the email address given a teamsid
@app.route('/api/get-user-by-id/<teamsid>', methods=['GET'])
def getuserbyid(teamsid):
    if WEBDEBUG:
        print_details(request)
    return(jsonify(email=teamsapi.getemailfromid(teamsurl,teamstoken,teamsid)))

# Returns a json representing the detailed information given a teamsid
@app.route('/api/get-detailed-info-by-id/<teamsid>', methods=['GET'])
def getdetailedinfo(teamsid):
    if WEBDEBUG:
        print_details(request)
    return(jsonify(teamsapi.getdetailedinfofromid(teamsurl,teamstoken,teamsid)))

# Returns a json representing if the email domain is in the white list database
@app.route('/api/get-email-domain/<domain>', methods=['GET'])
def getemaildomain(domain):
    if WEBDEBUG:
        print_details(request)
    print("Domain: " + domain)
    return(jsonify({"status":"not_implemented"}))

# Adds a domain to the white list database
@app.route('/api/post-email-domain/<domain>', methods=['POST'])
def postemaildomain(domain):
    if WEBDEBUG:
        print_details(request)
    print ("Domain: "+domain)
    return(jsonify({"status":"not_implemented"}))

# Returns a json representing if the endpoint id is in the white list database
@app.route('/api/get-endpoint-id/<deviceid>', methods=['GET'])
def getendpointid(deviceid):
    if WEBDEBUG:
        print_details(request)
    print("Device ID: " + deviceid)
    return(jsonify({"status":"not_implemented"}))

# Adds a device id to the white list database
@app.route('/api/post-endpoint-id/<deviceid>', methods=['POST'])
def postendpointid(deviceid):
    if WEBDEBUG:
        print_details(request)
    print ("Device ID: "+ deviceid)
    return(jsonify({"status":"not_implemented"}))

if __name__ == '__main__':
    app.run(debug=True)