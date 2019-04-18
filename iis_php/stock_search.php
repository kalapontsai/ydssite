<?php
require('./includes/oracle_oci_connect.php');
// https://www.php.net/manual/en/function.oci-close.php
$handle = fopen("logger.txt", "a");

$json_string = file_get_contents('visit_count.json');
$visit_count = json_decode($json_string, true);
$date = new DateTime();
//fwrite($handle,"test");
?>
<!DOCTYPE html>
<html>
<head>
  <title>庫存搜尋</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <link rel="shortcut icon" href="/statics/img/favicon.ico" type="image/x-icon">
  <link rel="icon" href="/statics/img/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" href="/statics/css/bootstrap.min.css">
  <link rel="stylesheet" href="/statics/css/style.css">
  <script type="text/javascript" src="/statics/js/jquery-3.3.1.min.js"></script>
  <script type="text/javascript" src="/statics/js/bootstrap.min.js"></script>
</head>
  <body> 
  <div class="container">
    <div class="row">
        <div class='col-lg-12'>
            <div class="center">
            <h1 class="center">物料搜尋</h1>
            <table class="TB_Bomlist">
                <caption> 至少一個欄位需填入搜尋字串,品名與規格的大小寫需注意</caption>
                <thead>
                  <tr>
                    <th>料號</th>
                    <th>品名</th>
                    <th>規格</th>
                    <th>FOX料號</th>
                    <th>庫存數</th>
                    <th>&nbsp;&nbsp;</th>
                  </tr>
                </thead>
                <tbody>
                  <form name="stock_serach" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method="post">
                  <tr>
                    <td><input type="text" name="qry_bom" size="16" value= "<?php if (isset($_POST['qry_bom'])) { echo $_POST['qry_bom'];} ?>" ></td>
                    <td><input type="text" name="qry_pn" size="16" value= "<?php if (isset($_POST['qry_pn'])) { echo $_POST['qry_pn'];} ?>" ></td>
                    <td><input type="text" name="qry_spec" size="16" value= "<?php if (isset($_POST['qry_spec'])) { echo $_POST['qry_spec'];} ?>" ></td>
                    <td><input type="text" name="qry_fox" size="16" value= "<?php if (isset($_POST['qry_fox'])) { echo $_POST['qry_fox'];} ?>" ></td>
                    <td><input type="text" name="qry_stock" size="16" value= "<?php if (isset($_POST['qry_stock'])) { echo $_POST['qry_stock'];} ?>" ></td>
                    <td><button type="summit" class="btn btn-primary"><span class="glyphicon glyphicon-search"></span>&nbsp;Search</button></td>
                  </tr>
                  </form>
                </tbody>
            </table>
            </div>
        </div>
    </div>
    <hr>
  <h4>範例 : 料號 : 10CP / 規格: 0805</h4>
  <h4>若要列出有庫存的料號,庫存數請輸入數字(預設為0)</h4>
<?php
  $conn = oci_connect(OCI_USER, OCI_PWD, OCI_HOST);
  if (!$conn) {
      $e = oci_error();
      trigger_error(htmlentities($e['message'], ENT_QUOTES), E_USER_ERROR);
  }
//模糊搜尋
//full query field string : "select if1.ima01,if1.ima02,if1.ima021,if1.ima25,if1.ima916,if1.imaud03,NVL(gf1.g10,0) from yuandean1.ima_file if1 left outer join (select img01 g1,sum(img10) g10 from yuandean1.img_file where img23='Y' group by img01) gf1 on (if1.ima01=gf1.g1) where ROWNUM < 1000"
  if ((isset($_POST['qry_bom'])) && (($_POST['qry_bom'] != "") || ($_POST['qry_pn'] != "") || ($_POST['qry_spec'] != "") || ($_POST['qry_fox'] != ""))) {
    $sql = "select if1.ima01,if1.ima02,if1.ima021,if1.imaud03,NVL(gf1.g10,0) from yuandean1.ima_file if1 left outer join (select img01 g1,sum(img10) g10 from yuandean1.img_file where img23='Y' group by img01) gf1 on (if1.ima01=gf1.g1) where ROWNUM < 1000";
    $sql_qry = "";
    if (isset($_POST['qry_bom']) && ($_POST['qry_bom'] != "")) { $sql_qry .= " and if1.ima01 like '%" . $_POST['qry_bom'] . "%' ";}
    if (isset($_POST['qry_pn']) && ($_POST['qry_pn'] != "")) { $sql_qry .= " and if1.ima02 like '%" . $_POST['qry_pn'] . "%' ";}
    if (isset($_POST['qry_spec']) && ($_POST['qry_spec'] != "")) { $sql_qry .= " and if1.ima021 like '%" . $_POST['qry_spec'] . "%' ";}
    if (isset($_POST['qry_fox']) && ($_POST['qry_fox'] != "")) { $sql_qry .= " and if1.imaud03 like '%" . $_POST['qry_fox'] . "%' ";}
    if (isset($_POST['qry_stock']) && ($_POST['qry_stock'] != "") && (is_numeric($_POST['qry_stock']))) { 
      $qry_stock = $_POST['qry_stock'];
    }
      else {
      $qry_stock = "0";
    }
    $sql .= $sql_qry . " and NVL(gf1.g10,0) >= " . $qry_stock . " order by 1";


    $stid = oci_parse($conn, $sql);
    oci_execute($stid);
    //echo "<p> $sql </p>";
    echo "<div class='row'><div class='col-lg-12'><table class='TB_DATA'><thead><tr><th>料號</th><th>品名</th><th>規格</th><th>舊料號</th><th>庫存數量</th></tr></thead><tbody>";
    $cont = 0;
    while (($row = oci_fetch_row($stid)) != false) {
        $cont += 1;
        echo "<tr>";
        echo "<td>" . $row[0] . "</td>" . "<td>" . $row[1] . "</td>" . "<td>" . $row[2] . "</td>" . "<td>" . $row[3] . "</td>" . "<td>" . $row[4] . "</td>";
        echo "</tr>";
    }
    echo "</tbody></table><p> 筆數 : $cont </p></div></div>";
    oci_free_statement($stid);
    oci_close($conn);

    $log = "[" . $date->format('Y-m-d H:i:sP') . "]: " . $_SERVER['REMOTE_ADDR'] . " :" . $sql_qry . "\r\n";
    fwrite($handle,$log);

    $visit_count['qry'] += 1;

  } // enf of if (isset($_GET['qry_bom']) ||
  else {
    $visit_count['visit'] += 1;
  }
  $visit_count['lastest modify'] = $date->format('Y-m-d H:i:sP');
  $fp = fopen('visit_count.json', 'w');
  fwrite($fp, json_encode($visit_count,JSON_PRETTY_PRINT));
  fclose($handle);
  fclose($fp); 
?>
</div></body></html>
