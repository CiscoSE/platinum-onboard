import requests
import json


def getemailfromid(url, token, personid):
    """

    @param url: url for the webex teams API calls
    @param token: WebEx Teams Token to be used for the queries of the WebEx Teams Cloud
    @param personid: personID of the end user that we would like to return the email to.
    @return: email address of the user with the id that is specified in the command line

    This function will take the personID value and query the WebEx Teams API to return the email address
    for that user.
    """
    info = getdetailedinfofromid(url, token, personid)
    if info == "":
        return ""
    else:
        return info['emails']


def getdetailedinfofromid(url, token, personid):
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

    # Set up the Headers based upon the WebEx Teams API
    headers = {'Authorization': 'Bearer {}'.format(token),
            'content-type': 'application/json'}

    # Send the request to the WebEx Teams API using the payload and headers defined above
    try:
        resp = requests.get(apistring, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return ''

    if resp.status_code == 200:

        message_dict = json.loads(resp.text)
        message_dict['statuscode'] = str(resp.status_code)

        return message_dict['items'][0]
    else:
        return ''


def createteamsroom(url, token, name):

    """

    @param url: url for the webex teams API calls
    @param token:  WebEx Teams Token to be used for the queries of the WebEx Teams Cloud
    @param name: name of the room that we will be created.

    This function will create a new Teams Room with the name specified in the command line.

    @return: if the request was successful, then return the id for the new room, otherwise return nothing
    """
    apistring = url+"/v1/rooms"

    # Set up the Headers based upon the WebEx Teams API
    headers = {'Authorization': 'Bearer {}'.format(token),
            'content-type': 'application/json'}

    bodydetails = '{"title": "'+name+'"}'

    try:
        resp = requests.request("POST",apistring, headers=headers,data=bodydetails)

    except requests.exceptions.RequestException as e:

        return ''

    if resp.status_code == 200:

        message_dict = json.loads(resp.text)

        return message_dict['id']
    else:
        return ''


def adduserstoroom(url, token, roomid, name):
    """

    @param url: url for the webex teams API calls
    @param token:  WebEx Teams Token to be used for the queries of the WebEx Teams Cloud
    @param roomid: id of the room that we want to people to
    @param name: The email address of the person to be added to the room.
    @return: returns the id of the request if successful otherwise nothing
    """

    apistring = url+"/v1/memberships"

    # Set up the Headers based upon the WebEx Teams API
    headers = {'Authorization': 'Bearer {}'.format(token),
            'content-type': 'application/json'}

    bodydetails = '{"roomId": "'+roomid+'","personEmail":"'+name+'"}'


    try:
        resp = requests.request("POST",apistring, headers=headers,data=bodydetails)

    except requests.exceptions.RequestException as e:
        print(e)
        return ''

    if resp.status_code == 200:

        message_dict = json.loads(resp.text)

        return message_dict['id'][0]
    else:
        return ''


def sendmessagetoroom(url, token, roomid, message):
    """

    @param url: url for the webex teams API calls
    @param token:  WebEx Teams Token to be used for the queries of the WebEx Teams Cloud
    @param roomid: id of the room that we want to people to
    @param message: message to send to the room
    @return: id if successful, otherwise nothing.

    This function will send a message to the room specified in the parameters.
    """

    apistring = url+"/v1/messages"

    # Set up the Headers based upon the WebEx Teams API
    headers = {'Authorization': 'Bearer {}'.format(token),
            'content-type': 'application/json'}

    bodydetails = '{"roomId": "'+roomid+'","markdown":"'+message+'"}'

    try:
        resp = requests.request("POST",apistring, headers=headers,data=bodydetails)

    except requests.exceptions.RequestException as e:
        print(e)
        return ''

    if resp.status_code == 200:

        message_dict = json.loads(resp.text)

        return message_dict['id'][0]
    else:
        return ''
