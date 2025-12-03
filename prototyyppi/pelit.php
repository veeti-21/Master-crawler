<?php

date_default_timezone_set('Europe/Helsinki');

$DATABASE_HOST = 'localhost';
$DATABASE_USER = 'root';
$DATABASE_PASS = '';
$DATABASE_NAME = 'vimmdb';

$con = mysqli_connect($DATABASE_HOST, $DATABASE_USER, $DATABASE_PASS, $DATABASE_NAME);
if (mysqli_connect_errno()) {
	exit('Failed to connect to MySQL: ' . mysqli_connect_error());
}


$sqlVimm = " SELECT * FROM games_list ORDER BY vimm_ID DESC ";
$resultVimm = $con->query($sqlVimm);

mysqli_close($con);
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Koontisivu vimm peleille</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
  
    <script src="index.js"></script>
<input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for names.." title="Type in a name">


<table id="myTable">
          <tr class="header">
            <th>kuva</th>
            <th>nimi</th>
            <th>linkki</th>
            <th>viimeisin haku</th>
          </tr>
          <?php 
          while($rows=$resultVimm->fetch_assoc()) { ?>
          <tr>
          <td><img class="tuoteKuva" src="uusin-malli.webp"></td>
            
          <td class="nimet"><?php echo $rows['vimm_nimi'];?></td>
            <td><a target="_blank" href="<?php echo $rows['vimm_linkki'];?>">Latauslinkki</a></td>
            <td><?php echo $rows['vimm_aika'];?></td>
  
            </tr>
          <?php
    }
    ?>
        </table>
		
		<script>
function myFunction() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
</script>
</body>
</html>
