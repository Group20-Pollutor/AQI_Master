<?php
class dataElements
{
 public $link='';
 function __construct($humidity, $temperature, $colevels, $co2levels, $noxlevels, $so2levels, $dustdensity)
 {
  $this->connect();
  $this->storeInDB($humidity, $temperature, $colevels, $co2levels, $noxlevels, $so2levels, $dustdensity); 
 }
 
 function connect(){
  $this->link = mysqli_connect('localhost','root','') or die('Cannot connect to the DB');
  mysqli_select_db($this->link,'pollutiondata') or die('Cannot select the DB');
 }
 
 function storeInDB($humidity, $temperature, $colevels, $co2levels, $noxlevels, $so2levels, $dustdensity)
 {
  $colevels  = $colevels/4.5 ;
  $co2levels = $co2levels/2;
  $noxlevels = $noxlevels/17;
  $so2levels = $so2levels/23;
  $query = "insert into pollutants set humidity='".$humidity."', temperature='".$temperature."', colevels='".$colevels."', co2levels='".$co2levels."', noxlevels='".$noxlevels."', so2levels='".$so2levels."', dustdensity='".$dustdensity."'";
  $result = mysqli_query($this->link,$query) or die('Errant query:  '.$query);
 }
 
}
if($_GET['humidity'] != '' and  $_GET['temperature'] != '')
{
 $dataElements = new dataElements($_GET['humidity'],$_GET['temperature'],$_GET['colevels'],$_GET['co2levels'],$_GET['noxlevels'],$_GET['so2levels'],$_GET['dustdensity']);
}
?>