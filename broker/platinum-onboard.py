import configparser
import teamsapi
import requests
from datetime import date
from utilities import print_details
from flask import Flask,jsonify,request,render_template
import db

print ("Platinum Onboard Engine Starting...\n")

print("Configuration Options:")
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
except configparser.NoOptionError:
    # Defaulting to the standard Spark API
    teamsurl = "https://api.ciscospark.com"

print ("teamsurl: "+teamsurl)

# This flag turns on debugging of the web messages hitting the flask server
try:
    debugmode = config.get("platinum-onboard","webdebug")
    if debugmode == 'True':
        WEBDEBUG = True
    else:
        WEBDEBUG = False
except configparser.NoOptionError:
    WEBDEBUG=False


try:
    teamstoken = config.get("platinum-onboard","token")
    provisionip = config.get("platinum-onboard","provision-ip")
    listenip = config.get("platinum-onboard","listen-ip")
    listenport = config.get("platinum-onboard","listen-port")

except:
    print("Error: Required items are not present in the configuration file.")
    exit(-1)

print("teamstoken : {HIDDEN}")
print("listenip: "+listenip)
print("listenport: "+listenport)
print("provision-ip: "+provisionip)
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

@app.route('/clear-tables')
def cleartables():

    ret,guestmsg = db.delete_database(dbname, "guest", "")
    if ret:
        guestmsg="Deleted"
    ret,domainmsg = db.delete_database(dbname, "domain", "")
    if ret:
        domainmsg="Deleted"
    ret,devicemsg = db.delete_database(dbname, "device", "")
    if ret:
        devicemsg="Deleted"
    return render_template("clear-tables.html", guest=guestmsg,domain=domainmsg,device=devicemsg)

@app.route('/clear-guesttable')
def clearguesttable():

    ret,guestmsg = db.delete_database(dbname, "guest", "")
    if ret:
        guestmsg="Deleted"
    return render_template("clear-tables.html", guest=guestmsg,domain="Not Deleted",device="Not Deleted")

@app.route('/add-device')
def dispdeviceadd():
    return render_template('device.html')


@app.route('/adddevice', methods=['POST', 'GET'])
def adddevice():
    if request.method == 'POST':

        deviceid = request.form['deviceid']

        ret, msg = db.insert_into_database(dbname, "device", NAME=deviceid)

    return render_template("result.html",msg = msg)

@app.route('/add-domain')
def dispdomainadd():
    return render_template('domain.html')


@app.route('/adddomain', methods=['POST', 'GET'])
def adddomain():
    if request.method == 'POST':

        domainid = request.form['domainid']

        ret, msg = db.insert_into_database(dbname, "domain", NAME=domainid)

    return render_template("result.html",msg = msg)

# Returns a json representing the email address given a teamsid
@app.route('/api/get-user-by-id', methods=['GET'])
def getuserbyid():
    if WEBDEBUG:
        print_details(request)

    if 'teamsid' not in request.args:
        return (jsonify({"result": "no parameter"}))
    return(jsonify(email=teamsapi.getemailfromid(teamsurl, teamstoken, request.args['teamsid'])))

# Returns a json representing the detailed information given a teamsid
@app.route('/api/get-detailed-info-by-id', methods=['GET'])
def getdetailedinfo():

    if WEBDEBUG:
        print ("Debugging")
        print_details(request)

    if 'teamsid' not in request.args:
        return (jsonify({"result": "no parameter"}))
    return(jsonify(teamsapi.getdetailedinfofromid(teamsurl, teamstoken, request.args['teamsid'])))

# Returns a json representing if the email domain is in the white list database
@app.route('/api/get-email-domain', methods=['GET'])
def getemaildomain():
    if WEBDEBUG:
        print_details(request)

    if 'domain' not in request.args:
        return (jsonify({"result": "no parameter"}))

    ret,msg = db.search_database(dbname, "domain", "name", request.args['domain'])
    return (jsonify({"result": msg}))

# Adds a domain to the white list database
@app.route('/api/post-email-domain', methods=['POST'])
def postemaildomain():
    if WEBDEBUG:
        print_details(request)
    if 'domain' not in request.args:
        return (jsonify({"result": "no parameter"}))
    ret,msg= db.insert_into_database(dbname, "domain", NAME=request.args['domain'])

    return(jsonify({"result":msg}))


# Returns a json representing if the endpoint id is in the white list database
@app.route('/api/get-endpoint-id', methods=['GET'])
def getendpointid():
    if WEBDEBUG:
        print_details(request)
    if 'deviceid' not in request.args:
        return (jsonify({"result": "no parameter"}))
    ret,msg = db.search_database(dbname, "device", "name", request.args['deviceid'])

    return(jsonify({"result":msg}))

# Adds a device id to the white list database
@app.route('/api/post-endpoint-id', methods=['POST'])
def postendpointid():
    if WEBDEBUG:
        print_details(request)

    if 'deviceid' not in request.args:
        return (jsonify({"result": "no parameter"}))
    ret, msg = db.insert_into_database(dbname, "device", NAME=request.args['deviceid'])

    return (jsonify({"result": msg}))

@app.route('/api/generate-guest-account',methods=['POST'])
def generateguestaccount():
    if WEBDEBUG:
        print_details(request)

    print (request.args)
    if ('deviceid' in request.args) and ('teamsid' in request.args):

        # Determine if deviceid is in white list

        deviceid=request.args['deviceid']
        ret, msg = db.search_database(dbname, "device", "name", deviceid)

        if (not ret):
            return(jsonify({"result": "deviceid not authorized"}))

        ret= teamsapi.getemailfromid(teamsurl, teamstoken, request.args['teamsid'])

        if ret=="":
            return (jsonify({"result": "teamsid not found"}))

        # Determine if emaildomain is in white list
        emailaddress=ret[0]
        print(emailaddress)
        emaildomain=emailaddress.split("@")[1]
        print (emaildomain)

        ret, msg = db.search_database(dbname, "domain", "name", emaildomain)

        if (not ret):
            return (jsonify({"result": "email domain not authorized"}))


        ret, msg = db.search_database(dbname, "guest", "name", emailaddress)

        if (ret):
            print(str(msg))
            print ("User "+emailaddress+" already has a account initiated!")

            if (msg['status']== 'initiated'):

                return (jsonify({"result": "initiated"}))
            else:
                return (jsonify({"result": "completed","password" : msg['guestpassword']}))

        # Trigger the initiation of the guest account create since the data is effective

        print("Create WebEx Teams Room with the new Password!")
        ret=teamsapi.createteamsroom(teamsurl, teamstoken,"Platinum Onboard Guest Wireless "+str(date.today())+" - "+emailaddress)
        if ret == '':
            print("Unable to create the teams room")
        else:
            roomId = ret

        print ("roomID="+roomId)
        ret=teamsapi.adduserstoroom(teamsurl, teamstoken,roomId,emailaddress)
        if ret == '':
            print("Unable to add people to the teams room")

        ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, roomId, "Welcome to the Platinum Onboard Service")
        ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, roomId, "We have initiated the creation of the guest wireless account for "+emailaddress)
        ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, roomId, "Please give us a few moments until your account is provisioned")


        print ("Triggering Guest Creation of '"+emailaddress+"' from device '"+deviceid+"' to "+provisionip)


        apistring = "http://64.121.80.249:8444/api/check-guest.php?emailid="+emailaddress
        print ("Sending API to trigger guest creation: "+apistring)
        # Set up the Headers based upon the Tropo API

        # Post the API call to the tropo API using the payload and headers defined above
        try:
            resp = requests.get(apistring)
        except requests.exceptions.RequestException as e:
            print(e)
            return (jsonify({"result": e}))

        if resp.status_code == 200:
            print (resp.text)

        else:
            return (jsonify({"result": "unable to send message to provisioning server"}))



        ret, msg = db.insert_into_database(dbname, "guest", NAME=emailaddress, DEVICE=deviceid, STATUS="initiated", TEAMSROOMID=roomId)


        if (not ret):
            # There was an issue with inserting the record.   This is a problem since we should role back the creation.
            return (jsonify({"result":msg}))
        else:
            # This was successful
            return (jsonify({"result": "success","record_id":msg}))

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

    if ('emailid' in request.args) and ('status' in request.args):

        emailid = request.args['emailid']

        if request.args['status']=="completed":
            if ('guestpassword' not in request.args):
                return(jsonify({"result":"no guest password"}))
            else:

                print ("Guest Password:"+request.args['guestpassword'])

                updatestring="STATUS='" + request.args['status'] + "', GUESTPASSWORD='"+request.args['guestpassword']+"'"

                print ("Emailid="+emailid)
                ret, msg = db.search_database(dbname, "guest", "name", emailid)
                print (msg['teamsroomid'])

                ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                 "Congratulations, Your account was successfully created!")
                ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                 "Your guest wireless password is: "+request.args['guestpassword'])


        else:
            updatestring = "STATUS='" + request.args['status'] + "'"

        ret, msg = db.update_database(dbname, "guest", updatestring, "NAME='" + request.args['emailid'] + "'")

        return (jsonify({"result":ret}))
    else:
        return (jsonify({"result":"wrong paramters"}))


if __name__ == '__main__':
    app.run(debug=True,host=listenip,port=listenport)