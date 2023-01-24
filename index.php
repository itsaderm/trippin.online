<?php
// Set the default refresh rate to 5 minutes
$refresh_rate = 300;

// Check if a "t" value is passed in the URL
if (isset($_GET['t'])) {
    // Convert the "t" value to minutes
    $refresh_rate = $_GET['t'] * 60;
}

// Set the refresh header
header("Refresh: $refresh_rate;");

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
