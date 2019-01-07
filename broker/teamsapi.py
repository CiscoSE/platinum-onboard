import requests
import json

def getemailfromid(url,token,personid):
    """

    @param url: url for the webex teams API calls
    @param token: WebEx Teams Token to be used for the queries of the WebEx Teams Cloud
    @param personid: personID of the end user that we would like to return the email to.
    @return: email address of the user with the id that is specified in the command line

    This function will take the personID value and query the WebEx Teams API to return the email address
    for that user.
    """
    info=getdetailedinfofromid(url,token,personid)
    if info == "":
        return ""
    else:
        return info['emails']


def getdetailedinfofromid(url,token,personid):
    """

    @param url: url for the webex teams API calls
    @param token: WebEx Teams Token to be used for the queries of the WebEx Teams Cloud
    @param personid: personID of the end user that we would like to return the email to.
    @return: Detailed array of all identification data for the user specifed by the personID field

    This function will take the person ID value and query the WebEx Teams API to return all data associated with the user.
    It includes:

    "avatar":
    "created":
    "displayName":
    "emails":
    "firstName":
    "id":
    "lastName":
    "nickName":
    "orgId":
    "type":

    """

    apistring = url+"/v1/people?id="+personid

    # Set up the Headers based upon the Tropo API
    headers = {'Authorization': 'Bearer {}'.format(token),
            'content-type': 'application/json'}


    # Post the API call to the tropo API using the payload and headers defined above
    try:
        resp = requests.get(apistring, headers=headers)
    except requests.exceptions.RequestException as e:
        print (e)
        return ''

    if resp.status_code == 200:

        message_dict = json.loads(resp.text)
        message_dict['statuscode'] = str(resp.status_code)

        return (message_dict['items'][0])
    else:
        return ''


def createteamsroom(url,token,name):


    apistring = url+"/v1/rooms"

    # Set up the Headers based upon the Tropo API
    headers = {'Authorization': 'Bearer {}'.format(token),
            'content-type': 'application/json'}

    bodydetails = '{"title": "'+name+'"}'

    try:
        resp = requests.request("POST",apistring, headers=headers,data=bodydetails)

        message_dict = json.loads(resp.text)
    except requests.exceptions.RequestException as e:

        return ''


    if resp.status_code == 200:

        message_dict = json.loads(resp.text)

        return (message_dict['id'])
    else:
        return ''


def adduserstoroom(url,token,roomid,name):


    apistring = url+"/v1/memberships"

    # Set up the Headers based upon the Tropo API
    headers = {'Authorization': 'Bearer {}'.format(token),
            'content-type': 'application/json'}

    bodydetails = '{"roomId": "'+roomid+'","personEmail":"'+name+'"}'


    try:
        resp = requests.request("POST",apistring, headers=headers,data=bodydetails)

        message_dict = json.loads(resp.text)

    except requests.exceptions.RequestException as e:
        print (e)
        return ''


    if resp.status_code == 200:

        message_dict = json.loads(resp.text)


        return (message_dict['id'][0])
    else:
        return ''

def sendmessagetoroom(url,token,roomid,message):


    apistring = url+"/v1/messages"

    # Set up the Headers based upon the Tropo API
    headers = {'Authorization': 'Bearer {}'.format(token),
            'content-type': 'application/json'}

    bodydetails = '{"roomId": "'+roomid+'","text":"'+message+'"}'

    try:
        resp = requests.request("POST",apistring, headers=headers,data=bodydetails)

        message_dict = json.loads(resp.text)

    except requests.exceptions.RequestException as e:
        print (e)
        return ''


    if resp.status_code == 200:

        message_dict = json.loads(resp.text)

        return (message_dict['id'][0])
    else:
        return ''