# Telepresense Endpoint API

## Introduction

The code in the directory is the service that listens for httpfeedback from Cisco telepresense
endpoints.  This module then contacts the Broker HTTP API to interact with the broker / core module
for all database and user creation functions.

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
