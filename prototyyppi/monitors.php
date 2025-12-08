<?php

date_default_timezone_set('Europe/Helsinki');

$DATABASE_HOST = 'placeholder';
$DATABASE_USER = 'placeholder';
$DATABASE_PASS = 'placeholder';
$DATABASE_NAME = 'placeholder';

$con = mysqli_connect($DATABASE_HOST, $DATABASE_USER, $DATABASE_PASS, $DATABASE_NAME);
if (mysqli_connect_errno()) {
	exit('Failed to connect to MySQL: ' . mysqli_connect_error());
}


$sqlNäytöt = " SELECT * FROM näytöt ORDER BY näytöt_ID DESC ";
$resultNäytöt = $con->query($sqlNäytöt);

mysqli_close($con);
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Koontisivu näytöille</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <script src="index.js"></script>


<table>
          <tr>
            <th>kuva</th>
            <th>nimi</th>
            <th>hinta</th>
            <th>linkki</th>
            <th>viimeisin haku</th>
          </tr>
          <?php 
          while($rows=$resultNäytöt->fetch_assoc()) { ?>
          <tr>
          <td><img class="tuoteKuva" src="uusin-malli.webp"></td>
            
          <td><?php echo $rows['näytöt_nimi'];?></td>
            <td><?php echo $rows['näytöt_hinta'];?></td>
            <td><a target="_blank" href="<?php echo $rows['näytöt_linkki'];?>">Linkki tuotesivulle</a></td>
            <td><?php echo $rows['näytöt_aika'];?></td>
  
            </tr>
          <?php
    }
    ?>
        </table>
</body>
</html>
