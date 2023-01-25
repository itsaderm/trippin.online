<?php
// Define the folder where the images are stored
$folder = "images/";

session_start();

// Check if the list of images is already stored in the session
if (!isset($_SESSION['images'])) {
    // Get a list of image files in the folder
    $_SESSION['images'] = array_values(array_diff(scandir($folder), array('.', '..')));
}

// Select a random image from the list stored in the session
$random_image = $_SESSION['images'][array_rand($_SESSION['images'])];

if(file_exists($folder.$random_image)){
    // Get the image from folder
    $image = file_get_contents($folder.$random_image);

    // Set the content type to image/webp
    header("Content-Type: image/webp");

    // Send the image to the client
    echo $image;
}else{
    header("Refresh:0");
}

?>
