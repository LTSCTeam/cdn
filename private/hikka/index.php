<?php

$dir = opendir(__DIR__);
function convert_bytes($size)
{
	$i = 0;
	while (floor($size / 1024) > 0) {
		++$i;
		$size /= 1024;
	}
 
	$size = str_replace('.', ',', round($size, 1));
	switch ($i) {
		case 0: return $size .= ' байт';
		case 1: return $size .= ' КБ';
		case 2: return $size .= ' МБ';
	}
}

?>

<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <meta http-equiv="x-ua-compatible" content="IE=edge">
  <title>Tokyani.space - Files</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="../assets/css/styles.css">
  <script type="text/javascript" src="../assets/js/jquery.min.js"></script>
</head>
  <h1>Directory:
/hikka/</h1>
  <table id="list">
    <thead>
      <tr>
        <th style="width:55%"><a href="?C=N&amp;O=A">File Name</a>&nbsp;<a href="?C=N&amp;O=D">&nbsp;↓&nbsp;</a></th>
        <th style="width:20%"><a href="?C=S&amp;O=A">File Size</a>&nbsp;<a href="?C=S&amp;O=D">&nbsp;↓&nbsp;</a></th>
        <th style="width:25%"><a href="?C=M&amp;O=A">Date</a>&nbsp;<a href="?C=M&amp;O=D">&nbsp;↓&nbsp;</a></th>
      </tr>
    </thead>
    <tbody>
        <?php
         while($name = readdir($dir)) {
            if ($name=='.' or $name=='..' OR $name == 'index.php')
               continue;
            echo '<tr>';
               print_r('<td class="link"><a href="'.$name.'"download="">'.$name.'</a></td>');
               print_r('<td class="link">');
               echo convert_bytes(filesize($name));
               print_r('</td>');
               print_r('<td class="link">');
               print_r(date("d F Y H:i:s", filemtime($name)));
               print_r('</td>');
             echo '</tr>';
        }
        ?>
    </tbody>
  </table>
  <div id="raw_include_README_md"></div>
  <script type="text/javascript" src="../assets/js/addNginxFancyIndexForm.js"></script>
  <script type="text/javascript" src="../assets/js/showdown.min.js"></script>
  <script type="text/javascript" defer="">
    var converter = new showdown.Converter();
    $("#raw_include_HEADER_md").load("HEADER.md", function() {
      var elem = document.querySelector("#raw_include_HEADER_md");
      var text = elem.innerHTML;
      text = text.replace(/\n[ ]*/g, '\n');
      var html = converter.makeHtml(text);
      elem.innerHTML = html;
    });
  </script>
</body>
</html>
