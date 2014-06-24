<?php
date_default_timezone_set('PRC');
function write_log($text)
{
	$resource = fopen("log.txt","a");
	fwrite($resource,date("Ymd H:i:s")." REMOTE_ADDR - $_SERVER[REMOTE_ADDR] ". $text . "\r\n");
	fclose($resource);
}
function do_upload($upload_dir, $file_name)
{
	$temp_name = $_FILES['wearingImage']['tmp_name'];
	$temp_name = $_FILES['wearingImage']['tmp_name'];
	//$file_name = $_FILES['upfile']['name'];
	$file_name = str_replace("\\","",$file_name);
	$file_name = str_replace("'","",$file_name);
	$file_path = $upload_dir.$file_name;

	//文件名字检查
	  if ( $file_name =="") {
		   $message = "Invalid File Name Specified";
		   return $message;
	  }

	  $result  =  move_uploaded_file($temp_name, $file_path);
	  if (!chmod($file_path,0755))
			$message = "change permission to 755 failed.";
	  else
			$message = ($result)?"$file_name uploaded successfully." :
				"Somthing is wrong with uploading a file.";
	  return $message;
}

function loader($url, $method = "get", $params = NULL){
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_HEADER, 0);
		
	if($method == "post"){
		curl_setopt($ch, CURLOPT_POST, 1);	
		curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
	}	
	
	$output = curl_exec($ch);
	
	if($output === FALSE){
		return FALSE;
	}
	
	$info = curl_getinfo($ch);
	curl_close($ch);

	return json_decode($output, true);
}
?>