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


$sqlGpu = " SELECT * FROM gpu ORDER BY gpu_ID DESC ";
$resultGpu = $con->query($sqlGpu);

mysqli_close($con);
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <link rel="stylesheet" href="style.css" />
    <title>Koontisivu näytönohjaimille</title>
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
          while($rows=$resultGpu->fetch_assoc()) { ?>
          <tr>
          <td><img class="tuoteKuva" src="uusin-malli.webp"></td>
            
          <td><?php echo $rows['gpu_nimi'];?></td>
            <td><?php echo $rows['gpu_hinta'];?></td>
            <td><a target="_blank" href="<?php echo $rows['gpu_linkki'];?>">Linkki tuotesivulle</a></td>
            <td><?php echo $rows['gpu_aika'];?></td>
  
            </tr>
          <?php
    }
    ?>
        </table>
</body>
</html>
