<?php
// Define the folder where the images are stored
$folder = "images/";

session_start();

// Get the t variable from the URL for the amount of minutes to wait before refresh, if null use 5 minutes default
$minutes = $_GET['t'] ?? 5;
$seconds = $minutes * 60;
header("Refresh: {$seconds}");

// Check if the list of images is already stored in the session
if (!isset($_SESSION['images']) || !isset($_SESSION['index_expiration']) || $_SESSION['index_expiration'] < time()) {
    // Get a list of image files in the folder
    $images = array_values(array_diff(scandir($folder), array('.', '..')));

    // Create an index of the images
    $index = array();
    foreach ($images as $image) {
        $index[$image] = sha1_file($folder . $image);
    }

    // Store the index and expiration date in the session
    $_SESSION['images'] = $index;
    $_SESSION['index_expiration'] = time() + (60 * 60);
    $_SESSION['displayed_images'] = array();
}

// Select a random image from the list stored in the session
$random_image = array_rand($_SESSION['images']);

while (in_array($random_image, $_SESSION['displayed_images'])) {
    $random_image = array_rand($_SESSION['images']);
}
$_SESSION['displayed_images'][] = $random_image;

if(file_exists($folder.$random_image)){
    // Get the image from folder
    $image = file_get_contents($folder.$random_image);

    // Disable caching of images
    header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
    header("Cache-Control: post-check=0, pre-check=0", false);
    header("Pragma: no-cache");    

    // Set the content type to image/webp
    header("Content-Type: image/webp");

    // Send the image to the client
    echo $image;
}else {
    header("Refresh:0");
}

// Destroy the session if all images have been displayed
if(count($_SESSION['images']) == count($_SESSION['displayed_images'])){
    session_destroy();
}
