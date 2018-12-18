### API Calls

GET {ip}/health

GET {ip}/api/get-user-by-id?teamsid=

GET {ip}/api/get-detailed-info-by-id?teamsid=

GET {ip}/api/get-email-domain?email=

POST {ip}/api/post-email-domain/?email=

GET {ip}/api/get-endpoint-id?deviceid=

POST {ip}/api/post-endpoint-id?deviceid=

#POST {ip}/api/generate-guest-account?deviceid=&email=

ToDo:
POST {ip}/api/generate-guest-account?deviceid={deviceid}&teamsid={teamsid}


GET {ip}/api/status-guest-account?email=

POST {ip}/api/update-status-guest-account?email=&status=



### Database Tables
#### domain
id
name
date

#### device
id
name
date

#### guest
id
name
device
date
status