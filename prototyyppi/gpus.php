<?php

date_default_timezone_set('Europe/Helsinki');

$DATABASE_HOST = 'localhost';
$DATABASE_USER = 'root';
$DATABASE_PASS = '';
$DATABASE_NAME = 'crawltest';

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
    <title>Koontisivu näytöille</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body onload="sorting()">
    <script src="index.js"></script>
<input type="text" id="myInput" onkeyup="myFunction()" placeholder="Search for names.." title="Type in a name">


<table id="myTable">
          <tr class="header">
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
            
          <td class="nimet"><?php echo $rows['gpu_nimi'];?></td>
            <td><?php echo $rows['gpu_hinta'];?></td>
            <td><a target="_blank" href="<?php echo $rows['gpu_linkki'];?>">Linkki tuotesivulle</a></td>
            <td><?php echo $rows['gpu_aika'];?></td>
  
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
// Source - https://stackoverflow.com/a
// Posted by Nick Grealy, modified by community. See post 'Timeline' for change history
// Retrieved 2025-12-03, License - CC BY-SA 4.0
function sorting(){
  const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

  const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
      v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
      )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

  // do the work...
  document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
      const table = th.closest('table');
      Array.from(table.querySelectorAll('tr:nth-child(n+2)'))
          .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
          .forEach(tr => table.appendChild(tr) );
})))};
</script>
      </body>
</html>
