import configparser
import teamsapi
from utilities import print_details
from flask import Flask,jsonify,request




print ("Platinum Onboard Engine Starting...\n")
WEBDEBUG=True
app = Flask(__name__)

# Open up the configuration file and get all application defaults
config = configparser.ConfigParser()
config.read('package_config.ini')

teamsurl = config.get("platinum-onboard","url")
teamstoken = config.get("platinum-onboard","token")


@app.route('/')
def index():
    if WEBDEBUG:
        print_details(request)
    return "Welcome to the Platinum Onboard Engine...\n"

@app.route('/api/testpost', methods=['POST'])
def testpost():
    if WEBDEBUG:
        print_details(request)
    return "Testing a post method"

@app.route('/api/get-user-by-id/<teamsid>', methods=['GET'])

def getuserbyid(teamsid):
    if WEBDEBUG:
        print_details(request)
    return(jsonify(email=teamsapi.getemailfromid(teamsurl,teamstoken,teamsid)))

@app.route('/api/get-detailed-info-by-id/<teamsid>', methods=['GET'])

def getdetailedinfo(teamsid):
    if WEBDEBUG:
        print_details(request)
    print(teamsapi.getdetailedinfofromid(teamsurl,teamstoken,teamsid))
    return(jsonify(teamsapi.getdetailedinfofromid(teamsurl,teamstoken,teamsid)))



if __name__ == '__main__':
    app.run(debug=True)