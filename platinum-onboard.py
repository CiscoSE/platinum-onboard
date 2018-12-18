import configparser
import teamsapi
from utilities import print_details
from flask import Flask,jsonify,request,render_template
import db

# This flag turns on debugging of the web messages hitting the flask server
WEBDEBUG=False

print ("Platinum Onboard Engine Starting...\n")

app = Flask(__name__,static_url_path='/static')

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
dbname="platinum-onboard.sqlite"
database = db.initialize_database(dbname)
if database == False:
    print ("Error: Unable to initialize the database.")
    exit(-1)

#
# Main Program Logic
#

# Route Point for generic message when web server is hit.
@app.route('/')
@app.route('/home.html')
def home():
    if WEBDEBUG:
        print_details(request)
    return render_template('home.html')

@app.route('/about')
def about():
    if WEBDEBUG:
        print_details(request)
    return render_template('about.html')


# Returns a json representing the state of the application server
@app.route('/health')
def apphealth():
    if WEBDEBUG:
        print_details(request)
    return jsonify({"health":"running"})

@app.route('/list-domain')
def listdomain():
    data = db.search_db(dbname, "domain")
    print (data)
    return render_template("list-domain.html", rows=data)

@app.route('/list-device')
def listdevice():
    data = db.search_db(dbname, "device")
    print (data)
    return render_template("list-device.html", rows=data)

@app.route('/list-guest')
def listguest():
    data = db.search_db(dbname, "guest")
    print (data)
    return render_template("list-guest.html", rows=data)

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

    ret,msg = db.search_database(dbname,"domain","name",domain)
    return (jsonify({"result": msg}))

# Adds a domain to the white list database
@app.route('/api/post-email-domain/<domain>', methods=['POST'])
def postemaildomain(domain):
    if WEBDEBUG:
        print_details(request)
    print ("Domain: "+domain)
    ret,msg=db.insert_into_database(dbname,"domain",NAME=domain)

    return(jsonify({"result":msg}))


# Returns a json representing if the endpoint id is in the white list database
@app.route('/api/get-endpoint-id/<deviceid>', methods=['GET'])
def getendpointid(deviceid):
    if WEBDEBUG:
        print_details(request)
    print("Device ID: " + deviceid)
    ret,msg = db.search_database(dbname,"device","name",deviceid)

    return(jsonify({"result":msg}))

# Adds a device id to the white list database
@app.route('/api/post-endpoint-id/<deviceid>', methods=['POST'])
def postendpointid(deviceid):
    if WEBDEBUG:
        print_details(request)
    print ("Device ID: "+ deviceid)
    ret, msg = db.insert_into_database(dbname, "device",NAME=deviceid)

    return (jsonify({"result": msg}))

@app.route('/api/generate-guest-account',methods=['POST'])
def generateguestaccount():
    if WEBDEBUG:
        print_details(request)

    print (request.args)
    if ('deviceid' in request.args) and ('email' in request.args):

        # Determine if deviceid is in white list

        deviceid=request.args['deviceid']
        ret, msg = db.search_database(dbname, "device", "name", deviceid)

        if (not ret):
            return(jsonify({"result": "not authorized"}))

        # Determine if emaildomain is in white list
        emailaddress=request.args['email']
        print(emailaddress)
        emaildomain=emailaddress.split("@")[1]
        print (emaildomain)

        ret, msg = db.search_database(dbname, "domain", "name", emaildomain)

        if (not ret):
            return (jsonify({"result": "not authorized"}))

        # Trigger the initiation of the guest account create since the data is effective

        ret, msg = db.insert_into_database(dbname,"guest",NAME=emailaddress,DEVICE=deviceid,STATUS="initiated")

        if (not ret):
            return (jsonify({"result": msg}))
        else:
            return (jsonify({"result":msg}))
    else:
        return (jsonify({"result": "wrong paramters"}))

@app.route('/api/status-guest-account',methods=['GET'])
def statusguestaccount():
    if WEBDEBUG:
        print_details(request)

    if 'email' not in request.args:
        return (jsonify({"result": "no parameter"}))
    else:
        emailaddress = request.args['email']
        ret, msg = db.search_database(dbname, "guest", "name", emailaddress)

        return (jsonify({"result":msg}))

@app.route('/api/update-status-guest-account',methods=['POST'])
def updatestatusguestaccount():
    if WEBDEBUG:
        print_details(request)

    return (jsonify({"result":"not implemented"}))


if __name__ == '__main__':
    app.run(debug=True)