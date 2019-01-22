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
```

Before  "sample-config.php" to "config.php"

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
