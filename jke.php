<?php
// vulnerable.php
 // test file
// ❌ 1. SQL Injection
$conn = new mysqli("localhost", "root", "password", "testdb");
$username = $_GET['username'];
$password = $_GET['password'];
$sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    echo "Welcome, $username!";
} else {
    echo "Invalid credentials!";
}

// ❌ 2. Cross-Site Scripting (XSS)
$search = $_GET['search'];
echo "<div>Search results for: $search</div>";

// ❌ 3. Remote Code Execution
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    // Dangerous function with unsanitized input
    system($cmd);
}

// ❌ 4. File Inclusion (LFI)
if (isset($_GET['page'])) {
    include($_GET['page']);
}

// ❌ 5. Insecure File Upload
if (isset($_FILES['file'])) {
    move_uploaded_file($_FILES['file']['tmp_name'], "uploads/" . $_FILES['file']['name']);
    echo "File uploaded!";
}

// ❌ 6. Information Disclosure
phpinfo();

?>
