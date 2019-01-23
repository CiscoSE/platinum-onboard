import configparser
import teamsapi
import requests
from datetime import date
from utilities import print_details
from flask import Flask,jsonify,request,render_template
import db

print("Platinum Onboard Engine Starting...\n")

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

print("teamsurl: "+teamsurl)

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
    print("Error: Unable to initialize the database.")
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


# Route point for displaying the about message
@app.route('/about')
def about():
    if WEBDEBUG:
        print_details(request)
    return render_template('about.html')


# Route point that returns a json representing the state of the application server
@app.route('/health')
def apphealth():
    if WEBDEBUG:
        print_details(request)
    return jsonify({"health":"running"})

# Route point that will dump the domain table and display the HTML
@app.route('/list-domain')
def listdomain():
    """
    Displays the domain table
    @return: html page of the table
    """
    data = db.search_db(dbname, "domain")
    return render_template("list-domain.html", rows=data)

# Route point that will dump the device table and display the HTML
@app.route('/list-device')
def listdevice():
    """
    Displays the device table
    @return: html page of the table
    """
    data = db.search_db(dbname, "device")
    return render_template("list-device.html", rows=data)

# Route point that will dump the guest table and display the HTML
@app.route('/list-guest')
def listguest():
    """
    Displays the guest table
    @return: html page of the table
    """
    data = db.search_db(dbname, "guest")
    return render_template("list-guest.html", rows=data)

# Route point that will clear all the tables and displays the result.
@app.route('/clear-tables')
def cleartables():
    """
    Clears all the database tables
    @return: html page to show status
    """

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

# Route point that will clear the guest table
@app.route('/clear-guesttable')
def clearguesttable():
    """
    Clears the guest table
    @return: html page to show status
    """
    ret,guestmsg = db.delete_database(dbname, "guest", "")
    if ret:
        guestmsg="Deleted"
    return render_template("clear-tables.html", guest=guestmsg,domain="Not Deleted",device="Not Deleted")

# Route point that will clear the domain table
@app.route('/clear-domaintable')
def cleardomaintable():
    """
    Clears the domain table
    @return: html page to show status
    """

    ret,domainmsg = db.delete_database(dbname, "domain", "")
    if ret:
        domainmsg="Deleted"
    return render_template("clear-tables.html", guest="Not Deleted",domain=domainmsg,device="Not Deleted")


# Route point that will clear the device table
@app.route('/clear-devicetable')
def cleardevicetable():
    """
    Clears the device table
    @return: html page to show status
    """

    ret,devicemsg = db.delete_database(dbname, "device", "")
    if ret:
        devicemsg="Deleted"
    return render_template("clear-tables.html", guest="Not Deleted",domain="Not Deleted",device=devicemsg)

# Route point that will allow the user to insert a new device id into a table
@app.route('/add-device')
def dispdeviceadd():
    """
    Displays the add device HTML page
    @return:
    """
    return render_template('device.html')

# Actual function to actually insert the data into the database which is called from the device.html
@app.route('/adddevice', methods=['POST', 'GET'])
def adddevice():
    """
    Adds a new device id into the database.

    @return:
    """
    if request.method == 'POST':

        deviceid = request.form['deviceid']

        ret, msg = db.insert_into_database(dbname, "device", NAME=deviceid)

    return render_template("result.html",msg = msg)

# Route point that will allow the user to insert a new domain id into a table
@app.route('/add-domain')
def dispdomainadd():
    """
    Display the add domain HTML page
    @return:
    """
    return render_template('domain.html')

# Actual function to actually insert the data into the database which is called from the domain.html
@app.route('/adddomain', methods=['POST', 'GET'])
def adddomain():
    """
    Adds a new domain to the white list database
    @return:
    """
    if request.method == 'POST':

        domainid = request.form['domainid']

        ret, msg = db.insert_into_database(dbname, "domain", NAME=domainid)

    return render_template("result.html",msg = msg)


# Returns a json representing the email address given a teamsid
@app.route('/api/get-user-by-id', methods=['GET'])
def getuserbyid():
    """
    Returns the email address of the user specified by the teamsid parameter
    @return:
    """
    if WEBDEBUG:
        print_details(request)

    if 'teamsid' not in request.args:
        return (jsonify({"result": "no parameter"}))
    return jsonify(email=teamsapi.getemailfromid(teamsurl, teamstoken, request.args['teamsid']))


# Returns a json representing the detailed information given a teamsid
@app.route('/api/get-detailed-info-by-id', methods=['GET'])
def getdetailedinfo():
    """
    Returns the detailed information about the user specified by the teamsid
    @return:
    """

    if WEBDEBUG:
        print("Debugging")
        print_details(request)

    if 'teamsid' not in request.args:
        return jsonify({"result": "no parameter"})
    return jsonify(teamsapi.getdetailedinfofromid(teamsurl, teamstoken, request.args['teamsid']))


# Returns a json representing if the email domain is in the white list database
@app.route('/api/get-email-domain', methods=['GET'])
def getemaildomain():
    """
    This function will see if an email domain is in the white list database
    @return: id of the record
    """
    if WEBDEBUG:
        print_details(request)

    if 'domain' not in request.args:
        return jsonify({"result": "no parameter"})

    ret,msg = db.search_database(dbname, "domain", "name", request.args['domain'])
    return jsonify({"result": msg})


# Adds a domain to the white list database
@app.route('/api/post-email-domain', methods=['POST'])
def postemaildomain():
    """
    This function will add a new domain to the white list database
    @return: result of the insert
    """
    if WEBDEBUG:
        print_details(request)
    if 'domain' not in request.args:
        return jsonify({"result": "no parameter"})
    ret,msg= db.insert_into_database(dbname, "domain", NAME=request.args['domain'])

    return jsonify({"result":msg})


# Returns a json representing if the endpoint id is in the white list database
@app.route('/api/get-endpoint-id', methods=['GET'])
def getendpointid():
    """
    This function will determine if a endpoint id already exists in the database.
    @return: id of the deviceid
    """
    if WEBDEBUG:
        print_details(request)
    if 'deviceid' not in request.args:
        return jsonify({"result": "no parameter"})
    ret,msg = db.search_database(dbname, "device", "name", request.args['deviceid'])

    return jsonify({"result":msg})


# Adds a device id to the white list database
@app.route('/api/post-endpoint-id', methods=['POST'])
def postendpointid():
    """
    This function will add a device id into the whitelist database
    @return: result of the insert
    """
    if WEBDEBUG:
        print_details(request)

    if 'deviceid' not in request.args:
        return jsonify({"result": "no parameter"})
    ret, msg = db.insert_into_database(dbname, "device", NAME=request.args['deviceid'])

    return jsonify({"result": msg})

# API Route point to generate a guest account create
@app.route('/api/generate-guest-account',methods=['POST'])
def generateguestaccount():
    """
    This function will trigger the process of a creation of a guest account.

    @return:
    """
    if WEBDEBUG:
        print_details(request)

    # This function must be called with both the deviceid parameter and the teamsid parameter
    if ('deviceid' in request.args) and ('teamsid' in request.args):

        # Determine if deviceid is in white list database.   If not, then the device isnt authorized to generate
        # guest account

        deviceid=request.args['deviceid']
        ret, msg = db.search_database(dbname, "device", "name", deviceid)

        if not ret:
            return jsonify({"result": "deviceid not authorized"})

        # Determine if the teamsid is a valid WebEx Teams user.   If not, then quit
        ret= teamsapi.getemailfromid(teamsurl, teamstoken, request.args['teamsid'])

        if ret=="":
            return jsonify({"result": "teamsid not found"})

        # Determine if emaildomain is in white list database, if not, then the email domain isn't authorized to generate
        # a guest account
        emailaddress=ret[0]
        emaildomain=emailaddress.split("@")[1]

        ret, msg = db.search_database(dbname, "domain", "name", emaildomain)

        if (not ret):
            return jsonify({"result": "email domain not authorized"})


        # Now that we know we are authorized, serach the guest table to determine if a guest account has already
        # been initiated
        ret, msg = db.search_database(dbname, "guest", "name", emailaddress)

        if (not ret):
            # Trigger the initiation of the guest account creation

            # Create a new teamsroom to communicate the status back to the user
            ret=teamsapi.createteamsroom(teamsurl, teamstoken,"Platinum Onboard Guest Wireless "+str(date.today())+" - "+emailaddress)
            if ret == '':
                print("Unable to create the teams room")
            else:
                roomId = ret

            # Add the user to the teams room that we just created
            ret=teamsapi.adduserstoroom(teamsurl, teamstoken,roomId,emailaddress)
            if ret == '':
                print("Unable to add people to the teams room")

            teamsapi.sendmessagetoroom(teamsurl, teamstoken, roomId,
                                            "--------------------------------------------------------")
            teamsapi.sendmessagetoroom(teamsurl, teamstoken, roomId, "**Welcome to the Platinum Onboard Service**")
            teamsapi.sendmessagetoroom(teamsurl, teamstoken, roomId, "We have initiated the creation of the guest wireless account for "+emailaddress)
            teamsapi.sendmessagetoroom(teamsurl, teamstoken, roomId, "Please give us a few moments until your account is provisioned")


            # Insert a new guest record into the database.
            ret, msg = db.insert_into_database(dbname, "guest", NAME=emailaddress, DEVICE=deviceid, STATUS="initiated", TEAMSROOMID=roomId)

            if (not ret):
                # There was an issue with inserting the record.  This is a problem since we should role back the creation.
                print("Unable to insert the record")
                return (jsonify({"result":msg}))
            else:
                print("Successful insertion of record")
                # This was successful

            # Send a request to the provisioning server
            print("Triggering Guest Creation of '"+emailaddress+"' from device '"+deviceid+"' to "+provisionip)

            apistring = "http://"+provisionip+"/api/check-guest.php?emailid="+emailaddress
            print("Sending API to trigger guest creation: "+apistring)

            # Post the API call to the provisioning engine

            resp = requests.post(apistring)
            print(str(resp))

            return jsonify({"result": "success", "record_id": msg})

        else:
            # User already has a guest account initiated:


            print(str(msg))
            print("User " + emailaddress + " already has a account initiated!")

            # Search the database for the record.

            ret, msg = db.search_database(dbname, "guest", "name", emailaddress)

            # If the status is initiated, then let the user know via the teams room, that we already initiated
            # a guest account.

            if (msg['status'] == 'initiated'):
                ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                 "--------------------------------------------------------")
                ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                 "Your account request was already initiated!")
                print("Initiated")
                return jsonify({"result": "initiated"})
            else:

                # Otherwise, the guest account is created, so end back the data concerning the wireless credentials

                ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                 "--------------------------------------------------------")
                ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                 "Your account was already provisioned:")
                ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                 "Guest Credentials are located below:")
                ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                 "ssid: **_platinum-guest_**")
                ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                 "username: **_" + emailaddress + "_**")
                ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                 "password: **_" + msg['guestpassword'] + "_**")

                print("Guest Password is: "+ msg['guestpassword'])
                return jsonify({"result": "completed", "password": msg['guestpassword']})

    else:
        print("Wrong Parameters")
        return jsonify({"result": "wrong paramters"})

# API Route point for retrieving the status of the guest account
@app.route('/api/status-guest-account',methods=['GET'])
def statusguestaccount():
    """
    This function will return the status of the guest account provided by the email address
    @return:  status
    """
    if WEBDEBUG:
        print_details(request)

    if 'email' not in request.args:
        return jsonify({"result": "no parameter"})
    else:
        emailaddress = request.args['email']
        ret, msg = db.search_database(dbname, "guest", "name", emailaddress)

        return jsonify({"result":msg})

# API Route point for updating the status of the guest account
@app.route('/api/update-status-guest-account',methods=['POST'])
def updatestatusguestaccount():
    """
    This function will update the status of the guest account
    @return:
    """
    if WEBDEBUG:
        print_details(request)

    # determine if both the emailid and status is provided in the request, if not, return the error value

    if ('emailid' in request.args) and ('status' in request.args):


        emailid = request.args['emailid']

        print("Emailid: "+emailid)

        # check to see if the status is completed.   If so, then we are going to ecxpect the guest password
        if request.args['status']=="completed":
            print("Status passed to function is completed")
            # If guest password is not passed to the parameter, then return an error message
            if ('guestpassword' not in request.args):
                print("Guestpassword is not passed to the function")
                return jsonify({"result":"no guest password"})
            else:

                print("Guest Password:"+request.args['guestpassword'])

                # Update the database record with the status and the guest password

                updatestring="STATUS='" + request.args['status'] + "', GUESTPASSWORD='"+request.args['guestpassword']+"'"

                # Search the database record to return the room id so we can alert the user.
                ret, msg = db.search_database(dbname, "guest", "name", emailid)

                # If guest record is found then send the message to the teams room

                if ret:
                    print(str(msg))
                    ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                     "--------------------------------------------------------")
                    ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                     "Congratulations, Your account was successfully created!")
                    ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                     "Guest Credentials are located below:")
                    ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                    "ssid: **_platinum-guest_**")
                    ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                    "username: **_"+emailid+"_**")
                    ret = teamsapi.sendmessagetoroom(teamsurl, teamstoken, msg['teamsroomid'],
                                                    "password: **_"+request.args['guestpassword']+"_**")
                else:
                    print("(Email id Found)")
                    return jsonify({"result": "emailid not found"})


        else:

            # Update the status of the record.
            updatestring = "STATUS='" + request.args['status'] + "'"

        ret, msg = db.update_database(dbname, "guest", updatestring, "NAME='" + request.args['emailid'] + "'")
        print(str(msg))

        return jsonify({"result":ret})
    else:
        return jsonify({"result":"wrong paramters"})


if __name__ == '__main__':
    app.run(debug=True,host=listenip,port=listenport)