<html>
 <head>
 </head>
 <body>
 <h1>Database info</h1>

 <?php
 Print "Hello, World! I am a web server and my hostname is: ";
 echo exec('hostname');
 Print  "</p>";
                echo  "List of Databases: </BR>";
        $link = mysqli_connect(getenv('DB_HOST'), getenv('DB_USER'), getenv('DB_PASSWORD')) or die(mysqli_connect_error($link));
        $res = mysqli_query($link, "SHOW DATABASES;");
        while ($obj = mysqli_fetch_object($res)) {
          printf ("%s</br>", $obj->Database);
        }
?>


</body>
</html>