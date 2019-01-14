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
	//$output = trim($output,'[]');
	$data = json_decode($output,TRUE);
	//pa($data);
	logit("debug:\n" . print_r($output,true));
	logit("debug:\n" . print_r($data,true));
	return $data;
}

//Post Back Message
function send_confirm_options_popup($ip,$sessionId,$users=array()){

	$url = "https://$ip/putxml";  
	$ch = curl_init();  
	$string = 
	"<Command>
		<UserInterface>
			<Message>
				<Prompt>
					<Display>
						<Duration>30</Duration>
						<FeedbackId>"; $string.= $users[0]['UserId']['Value']; $string.= "</FeedbackId>
						<Option.1>I am NOT Listed</Option.1>";
						//pa($users);
						/*
						$i = 2;
						foreach($users as $a=>$b){
							$string .= "<Option.$i>" + $b['Name']['Value'] + "</Option.$i>\n";
							//pa($b['Name']['Value']);
							//pa($b);
							//logit("Iteration $i" + print_r($a,true));
							break;
							$i++;
						}
						*/
						//work around
						$string .= "<Option.2>"; $string .= $users[0]['Name']['Value']; $string .= "</Option.2>";
						
						
						$string .= '<Text>Are you Listed?</Text>';
						$string .= "<Title>Please Confirm Your Identity</Title>
					</Display>
				</Prompt>
			</Message>
		</UserInterface>
	</Command>";
	
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Cookie: SecureSessionId=$sessionId"));
	curl_setopt($ch, CURLOPT_URL, $url); 
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($ch, CURLOPT_HEADER, array('Content-Type:application/xml'));  
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $string);	

	$output = curl_exec($ch);
	
	//logit($string);
	//logit($output);
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

//sends a message indicating the the user creation request was successful
function send_confirmation_message($ip,$sessionId){
	global $username; global $password;
	$url = "https://$ip/putxml";  
	$ch = curl_init();  
	$string = 
	'<Command>
		<UserInterface>
			<Message>
				<Prompt>
					<Display>
						<Duration>15</Duration>
						<FeedbackId>user_created</FeedbackId>
						<Option.1>Ok</Option.1>
						<Text>Please look for a new Space in Webex Teams with network credentials Shortly.</Text>
						<Title>Your Access Request Has Been Recieved and is Being Processed.</Title>
					</Display>
				</Prompt>
			</Message>
		</UserInterface>
	</Command>';
	 
	curl_setopt($ch, CURLOPT_USERPWD, "$username:$password");
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Cookie: SecureSessionId=$sessionId"));
	curl_setopt($ch, CURLOPT_URL, $url); 
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
	curl_setopt($ch, CURLOPT_HEADER, array('Content-Type:application/xml'));  
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $string);	

	$output = curl_exec($ch);
	//logit("Debug: CONFIRM CREATE");
	//logit($output);
	return $output;
}


//sends a message that the new user request has been initiated
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
						<Text>Your new user account request has been initiated.  You will recieve a message in Webex Teams when it has been provisioned.</Text>
						<Title>User Account Submitted</Title>
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
	//logit("debug:\n" . print_r($output,true));
	
}

?>