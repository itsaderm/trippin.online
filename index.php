/* I fucking hate PHP, and I didn't even write the code */

<?php
// Define the folder where the images are stored
$folder = "images/";

session_start();

// Get the `t` variable from the URL for the amount of minutes to wait before refresh, default to 5 minutes
$minutes = $_GET['t'] ?? 5;
$seconds = $minutes * 60;
header("Refresh: {$seconds}");

// Set the page title in PHP (this will only affect HTTP headers, not the browser tab title)
// Using an alternative approach to set a page title in PHP-only mode
header('X-Page-Title: trippin.online');

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
    $_SESSION['index_expiration'] = time() + (60 * 60); // 1 hour
    $_SESSION['displayed_images'] = array();
}

// Select a random image from the list stored in the session
$random_image = array_rand($_SESSION['images']);

while (in_array($random_image, $_SESSION['displayed_images']) && count($_SESSION['displayed_images']) < count($_SESSION['images'])) {
    $random_image = array_rand($_SESSION['images']);
}

// Add the chosen image to the displayed list
$_SESSION['displayed_images'][] = $random_image;

// Check if the image file exists
if (file_exists($folder . $random_image)) {
    // Get the image extension to determine the correct MIME type
    $image_ext = pathinfo($random_image, PATHINFO_EXTENSION);
    $mime_type = 'image/' . ($image_ext === 'webp' ? 'webp' : ($image_ext === 'jpg' || $image_ext === 'jpeg' ? 'jpeg' : 'png'));

    // Get the image from the folder
    $image = file_get_contents($folder . $random_image);

    // Disable caching of images
    header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
    header("Cache-Control: post-check=0, pre-check=0", false);
    header("Pragma: no-cache");

    // Set the content type based on the image extension
    header("Content-Type: $mime_type");

    // Send the image to the client
    echo $image;
} else {
    // Redirect to refresh if the image does not exist
    header("Refresh:0");
    exit();
}

// Destroy the session if all images have been displayed
if (count($_SESSION['images']) === count($_SESSION['displayed_images'])) {
    session_destroy();
}
?>
