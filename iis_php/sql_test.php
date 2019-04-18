<?php  
$serverUrl = "0.0.0.0";
$connInfo = array( "Database"=>"xxx", "UID"=>"xxx", "PWD"=>"xxxxx", "CharacterSet" => "UTF-8");
$conn = sqlsrv_connect( $serverUrl, $connInfo);
if( $conn ) {  
 echo "Connection succeeded.";
}else{
 echo "Connection failed.";
 die( print_r( sqlsrv_errors(), true));
}

sqlsrv_close($conn);  
?>