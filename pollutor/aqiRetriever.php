<?php

$dbname = 'pollutiondata';
$dbuser = 'root';  
$dbpass = ''; 
$dbhost = 'localhost'; 

$connect = @mysqli_connect($dbhost,$dbuser,$dbpass,$dbname);

$query = "select * from aqi_table order by id desc limit 1";

$rawData = mysqli_query($connect , $query); 

while ($result = mysqli_fetch_assoc($rawData))
{
	$jsonData[] = $result;
}

print json_encode($jsonData, JSON_NUMERIC_CHECK);

?>