<?php

//Errors on but notices off.  
//Notices can screw up the http reply sent to the codec when it sends httpfeedback
error_reporting(E_ALL & ~E_NOTICE);

//endpoint credentials
$user = 'user';
$pass = 'cisco';

include('./config.php');
include ('./functions.php');

//read posted JSON data from codec's httpfeedback system
$data = file_get_contents('php://input');
//logit($data); //Used when debugging to see the full format of the data as its posted

$event = json_decode($data,TRUE);
//logit($event);//Used when debugging to see the full format of the data after converting to array

//get IP address of codec thats making requests to this API
if(isset($event['Event']['Identification']['IPAddress']['Value'])){
	$ip = $event['Event']['Identification']['IPAddress']['Value'];
}else{
	exit();//only hit when malformed requests are sent
}


//Authenticate to the calling endpoint
if(!$secureSessionId = authenticate_web($ip,$user,$pass)){
	logit("Failed to Authenticate to the video endpoint: $ip");
	exit();
}

//If the "Network Registration" button is clicked
if($event['Event']['UserInterface']['Extensions']['Panel']['Clicked']['PanelId']['Value'] == "register" ){
	
	//verify a user is paired via Proximity.  If so reply with a confirmation.  Else reply with a notice. 
	if($users = get_paired_users($ip,$secureSessionId)){
		send_confirm_options_popup($ip,$secureSessionId,$users);
	}else{
		send_no_webex_pair($ip,$secureSessionId);
	}
}

//If the "Yes, I am XYZ" user button is pressed attempt to create the user
if($event['Event']['UserInterface']['Message']['Prompt']['Response']['OptionId']['Value'] == 2 ){
	//logit("response recieved");
	$userId = $event['Event']['UserInterface']['Message']['Prompt']['Response']['FeedbackId']['Value'];
	$deviceId = $event['Event']['Identification']['SerialNumber']['Value'];
	if($result = create_user($userId,$deviceId)){
		$val = json_decode($result,true);
		logit("A user with the teams id of: $userId was requested with result code of: " . $val['result']);
	}else{
		logit("Failed to create user with teams id of: $userId");
	}
}


//close the authentication session with the endpoint
terminate_session_web($ip,$secureSessionId);

?>