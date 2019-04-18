<html>
<head>
</head>
<body>
<h2>PHP in IIS</h2>

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

$sql="select * from TestUnit";
$result=sqlsrv_query($conn,$sql)or die("sql error".sqlsrv_errors());
      
echo "讀取test unit的值：<br />";
while($row=sqlsrv_fetch_array($result)){
     echo ("<table border=1px><tr>");
     echo ("<td>col：").$row["col"].("</td>");
     echo ("<td>unit：").$row["unit"].("</td>");
     echo ("<td>name：").$row["name"].("</td>");
     echo ("</tr></table>");
     echo ("<hr />");
       }
sqlsrv_close($conn);
?>

</body>
</html>"
