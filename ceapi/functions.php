<?php

/********************************************
*
*  Utility Functions for troubleshooting, etc
*
********************************************/

//logs to a file
function logit($string){
	if(is_array($string)){ $string = print_r($string,true);}
	$timestamp = date("d/M/Y:H:i:s P");
	file_put_contents("./log","[$timestamp] $string\n",FILE_APPEND);
	//echo "test";
}

//better format array outputs on html pages
function pa($var, $mode = "text"){
	if($mode = "text") {print_r($var);}
	else {echo "<pre>"; print_r($var); echo "</pre>";}
}


/********************************************
*
*Functions for calling the video endpoint API
*
********************************************/

//authentication with the end point and return SecureSessionId
function authenticate_web($ip,$username,$password){

	$ch = curl_init("https://$ip/xmlapi/session/begin");
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_POST, 1);
	curl_setopt($ch, CURLOPT_HEADER, 1);
	curl_setopt($ch, CURLOPT_USERPWD, "$username:$password");
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
	$result = curl_exec($ch);
	preg_match_all('/^Set-Cookie:\s*([^;]*)/mi', $result, $matches);
	$cookies = array();
	foreach($matches[1] as $item) {
		parse_str($item, $cookie);
		$cookies = array_merge($cookies, $cookie);
	}
	 //var_dump($cookies); 
	 curl_close($ch);
	 if(isset($cookies['SecureSessionId'])){
		return $cookies['SecureSessionId'];
	 }else{
		 return false; //ie authentication failed in some way
	 }
	 


}

//End the session started by authenticate_web
function terminate_session_web($ip,$sessionId){
	
	//$ch = curl_init("https://$ip/xmlapi/session/end");  //Not used
	$ch = curl_init("https://$ip/web/signin/signout");
	
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_HEADER, 1);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, false );	
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Cookie: SecureSessionId=$sessionId"));
	
	$result = curl_exec($ch);
	curl_close($ch);

}

//returns array of the users Proximity paired with the system if any
function get_paired_users($ip,$sessionId){

	$url = "https://$ip/web/api/status/Spark/PairedDevice";  
	$ch = curl_init();  
	curl_setopt($ch, CURLOPT_URL, $url); 
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Cookie: SecureSessionId=$sessionId"));
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

	$output = curl_exec($ch);
	curl_close($ch);
	//pa($output);
	$output = trim($output,'[]');
	$data = json_decode($output,TRUE);
	//pa($data);
	return $data;
}

//Post Back Message
function send_confirm_options_popup($ip,$sessionId,$users=array()){

	$url = "https://$ip/putxml";  
	$ch = curl_init();  
	$string = 
	'<Command>
		<UserInterface>
			<Message>
				<Prompt>
					<Display>
						<Duration>60</Duration>
						<FeedbackId>' . $users['UserId']['Value'] . '</FeedbackId>
						<Option.1>I am NOT</Option.1>
						<Option.2>Yes, I am ' . $users['Name']['Value'] . '</Option.2>
						<Text>Are you ' . $users['Name']['Value'] . '?</Text>
						<Title>Please Confirm Your Identity</Title>
					</Display>
				</Prompt>
			</Message>
		</UserInterface>
	</Command>';
	
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Cookie: SecureSessionId=$sessionId"));
	curl_setopt($ch, CURLOPT_URL, $url); 
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($ch, CURLOPT_HEADER, array('Content-Type:application/xml'));  
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $string);	

	$output = curl_exec($ch);
	
	return $output;
}

//sends and error message to the endpoint indicating that no user is paired
function send_no_webex_pair($ip,$sessionId){

	$url = "https://$ip/putxml";  
	$ch = curl_init();  
	$string = 
	'<Command>
		<UserInterface>
			<Message>
				<Prompt>
					<Display>
						<Duration>15</Duration>
						<FeedbackId>pairing_error</FeedbackId>
						<Option.1>Ok</Option.1>
						<Text>Please Pair with the device via Webex Teams Proximity</Text>
						<Title>No User Paired</Title>
					</Display>
				</Prompt>
			</Message>
		</UserInterface>
	</Command>';
	
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Cookie: SecureSessionId=$sessionId"));
	curl_setopt($ch, CURLOPT_URL, $url); 
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($ch, CURLOPT_HEADER, array('Content-Type:application/xml'));  
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $string);	

	$output = curl_exec($ch);
	
	return $output;
}


//sends a message that the user is already initiated
function send_user_initiated($ip,$sessionId){

	$url = "https://$ip/putxml";  
	$ch = curl_init();  
	$string = 
	'<Command>
		<UserInterface>
			<Message>
				<Prompt>
					<Display>
						<Duration>15</Duration>
						<FeedbackId>user_initiated</FeedbackId>
						<Option.1>Ok</Option.1>
						<Text>Your user account request has already been initiated.  You will recieve a message in Webex Teams when it has been provisioned.</Text>
						<Title>User Already Initiated</Title>
					</Display>
				</Prompt>
			</Message>
		</UserInterface>
	</Command>';
	
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Cookie: SecureSessionId=$sessionId"));
	curl_setopt($ch, CURLOPT_URL, $url); 
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($ch, CURLOPT_HEADER, array('Content-Type:application/xml'));  
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $string);	

	$output = curl_exec($ch);
	
	return $output;
}

/********************************************
*
*    Functions for calling the Core API
*
********************************************/

//sends a user creation request to the core application
function create_user($userId,$deviceId){
	global $broker;
	$query =  "api/generate-guest-account?deviceid=$deviceId&teamsid=$userId";	
	$url = "http://$broker/" . $query;  
	$ch = curl_init(); 
	
	curl_setopt($ch, CURLOPT_URL, $url); 
	curl_setopt($ch, CURLOPT_POST, 1);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

	$output = curl_exec($ch);
	curl_close($ch);
	
	return $output;
	
}

?>