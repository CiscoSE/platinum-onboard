import requests
import json

def getemailfromid(url,token,id):

    apistring = url+"/v1/people?id="+id

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

            return(message_dict['items'][0]['emails'][0])
        else:
            return ''


def getdetailedinfofromid(url,token,id):

    apistring = url+"/v1/people?id="+id

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
        print (message_dict)
        message_dict['statuscode'] = str(resp.status_code)

        return (message_dict['items'][0])
    else:
        return ''
