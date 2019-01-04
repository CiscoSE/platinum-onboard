## Telepresense Endpoint API

The code in the directory is the service that listenes for httpfeedback from telepresense endpoints.
This module then contacts an HTTP API to interact with the broker / core module for all database and 
user creation functions. 

Before use edit to your needs and rename "sample-config.php" to "config.php"

On your video endpoint you will need to enable HTTP Feedback.  Use the CLI command below substituting 
the IP / Hostname of your CEAPI service.

xcommand HttpFeedback Register FeedbackSlot: 1 
Expression: /Event/UserInterface/Extensions/Panel/Clicked 
Expression: /Event/UserInterface/Message/Prompt/Response 
Format: JSON 
ServerUrl: http://<ip address>/platinum-onboard/ceapi/


You can verify the feedback registration with the "xstatus HttpFeedback" command


xstatus HttpFeedback
*s HttpFeedback 1 Expression 1: "/Event/UserInterface/Extensions/Panel/Clicked"
*s HttpFeedback 1 Expression 2: "/Event/UserInterface/Message/Prompt/Response"
*s HttpFeedback 1 Format: "JSON"
*s HttpFeedback 1 Status: OK
*s HttpFeedback 1 URL: "http://10.100.210.15/platinum-onboard/ceapi/"
** end

OK



 
