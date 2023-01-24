<?php
if(isset($_GET['t']) && is_numeric($_GET['t'])) {
    $refresh_time = $_GET['t'];
} else {
    $refresh_time = 180;
}
header("Refresh: {$refresh_time};");

// Set the content type to image/jpeg
header("Content-Type: image/jpeg");

// Define the folder where the images are stored
$folder = "images/";

// Get a list of image files in the folder
$images = scandir($folder);

// Create an array to store the images that have been displayed
session_start();
if(!isset($_SESSION['displayed_images'])){
    $_SESSION['displayed_images'] = array();
}

// Select a random image from the list
do{
    $i = rand(2, count($images)-1);
    $image = $folder.$images[$i];
}while(in_array($image, $_SESSION['displayed_images']));

// Add the selected image to the array of displayed images
$_SESSION['displayed_images'][] = $image;

// Send the image to the client
readfile($image);
?>
