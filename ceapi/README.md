# Telepresense Endpoint API

## Introduction

The code in the directory is the service that listens for httpfeedback from Cisco telepresense
endpoints.  This module then contacts the Broker HTTP API to interact with the broker / core module
for all database and user creation functions.

## Functionality

This module performs the key functions between the Cisco Endpoints registered to the Cisco Webex Cloud
and the Broker module.  As you can see in the architecture diagram the Video endpoints, when configured
as described below, will make API calls to this module the the form of httpfeedback requests.  This
module will then in turn make API requests to an undocumented API of the endpoint to query for additional
information.  The information collected is the Webex Teams ID of the users paired with the video endpoint.  
This module will also use the documented XAPI to generate popup messages and prompts on the screen of the
endpoint for the user to interact with while registering.

The architecture diagram below shows this module in the upper left.  This module and the endpoints make
requests to each other while this module only make requests to the broker.  The broker always replys with
detailed results on which this module will log the results and push an on screen notification to the
video endpoint originating the request.

**Architecture:**
![Architecture](img/architecture.png)

## The Undocumented API

The undocumented API is in fact the API that is used to build the web GUI interface when administering
the endpoint.  This API is not documented by Cisco, is not supported at this time, and is subject to change
in functionality and format in the future.

To understand this API, browser-based development tools were used to watch the http requests as the
web admin GUI was loaded.  The reverse engineering process was trial and error based.  The root of the
API is *https://{ip address}/web/api/*.  This application pruned the resulting data by using the more
specific *https://{ip address}/web/api/status/Spark/PairedDevice*.  The data is returned in JSON format
and then parsed into an array by this module.

## Configuration / Service Setup

To install this application prepare a unix based Apache / PHP Server in follow the guide below.
In this guide we will assume the default server directory is /var/www/html

1. Copy all PHP files in this CEAPI directory to your web server.
```
cd ./platinum-onboard/ceapi
cp *.php /var/www/html
```
2. Create the configuration file from the sample-config.php file.  Edit the file
as needed for your environment.
```
cp sample-config config.php
nano config.php
```
3. Edit the file according to your needs.  The username and password are for authentication
to your video endpoints.  The application must authenticate to your endpoints to extract the
teams ID needed to create a user account.  These credential must have admin level access
on the video endpoint.
The "Broker" variable can be an IP address and port number for the borker service.  This is
the address the CEAPI code will make API calls to to ultimately create user accounts.
The broker can run on the same system (on a different tcp port 127.0.0.1) or a remote system.
You can see the sample configuration file contents below:

```php

//telepresense endpoint service account username and password
//must be admin
$username = 'username';  
$password = "password";

//The broker service IP address and port number if not 80
$broker = "192.168.1.11:8080";
```
4. The CEAPI generates a log file to assist in troubleshooting and development. To
use this file you have to create it and enable it to be written to by the Apache user.

```
touch log
chmod +w log
```


### Video Endpoint Setup

First, you will need to import the xml file to your video endpoint's in room controls.  This
provides the GUI button to allow registrants to start the process.  


Next, on your video endpoint you will need to enable HTTP Feedback.  Use the CLI command below
substituting the IP / Hostname of your CEAPI service.

xcommand HttpFeedback Register FeedbackSlot: 1
Expression: /Event/UserInterface/Extensions/Panel/Clicked
Expression: /Event/UserInterface/Message/Prompt/Response
Format: JSON
ServerUrl: http://<ip address>/platinum-onboard/ceapi/


You can verify the feedback registration with the "xstatus HttpFeedback" command

```
xstatus HttpFeedback
*s HttpFeedback 1 Expression 1: "/Event/UserInterface/Extensions/Panel/Clicked"
*s HttpFeedback 1 Expression 2: "/Event/UserInterface/Message/Prompt/Response"
*s HttpFeedback 1 Format: "JSON"
*s HttpFeedback 1 Status: OK
*s HttpFeedback 1 URL: "http://10.100.210.15/platinum-onboard/ceapi/"
** end

OK
```
