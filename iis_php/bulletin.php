<!DOCTYPE html>
<html>
<head>
  <title>生產佈告欄</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <link rel="shortcut icon" href="/statics/img/favicon.ico" type="image/x-icon">
  <link rel="icon" href="/statics/img/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" href="/statics/css/bootstrap.min.css">
  <link rel="stylesheet" href="/statics/css/style_bulletin.css">
  <script type="text/javascript" src="/statics/js/jquery-3.3.1.min.js"></script>
  <script type="text/javascript" src="/statics/js/bootstrap.min.js"></script>
  <script type="text/javascript">
    function clk() {
      var a=new Date();
      var a_month = a.getMonth() + 1;
      document.getElementById("time_now").innerHTML = a.getFullYear() + "/" + (a.getMonth() + 1) + "/" + a.getDate() + "  " + a.getHours() + ":" + a.getMinutes() + ":" + a.getSeconds() ;
    }
    function data_list() {
    	var x = document.getElementById("content").rows[0].cells;
    	$.getJSON('index_json.php', function(data) {
    		//alert(data.feeds[0].field6.replace("\r\n\r\n", ""));
    		// x[0].innerHTML = data.feeds[0].created_at;
    		console.log(data);
    		x[1].innerHTML = data[0].col;
    		x[2].innerHTML = data[0].unit;
    		x[3].innerHTML = data[0].name;
		});
     
    }
    </script>
</head>
<body onLoad="setInterval(clk, 1000); data_list();">
<div class="outer">
	<div class="container-fluid">
		<div class="row">
			<div class="col-md-8">
				<h1 class="center"><b>YDS Mfg Bulletin 生產看板</b></h1>
			</div>
			<div class="col-md-4">
				<h3 class="right"><div id='time_now'>00:00:00</div></h3>
			</div>
		</div>
		<div class="row">
			<div class="col-md-6">
				<table class="TB_bulletin table-striped">
					<caption>Dep1</caption>
					<thead>
						<tr>
							<th>na</th><th>Col</th><th>Unit</th><th>Name</th>
						</tr>
					</thead>
					<tbody id="content">
							<tr>
								<td>AAA</td><td>100</td><td>99</td><td>99%</td>
							</tr>
							
					</tbody>
				</table>
			</div>
			<div class="col-md-6">
				<table class="TB_bulletin table-striped">
					<caption>Dep2</caption>
					<thead>
						<tr>
							<th>機種</th><th>計劃數量</th><th>目前進度</th><th>完成度</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>AAA</td><td>100</td><td>99</td><td>99%</td>
						</tr>
						<tr>
							<td>BBB</td><td>200</td><td>100</td><td>50%</td>
						</tr>
						<tr>
							<td>AAA</td><td>100</td><td>99</td><td>99%</td>
						</tr>
						<tr>
							<td>BBB</td><td>200</td><td>100</td><td>50%</td>
						</tr>
						<tr>
							<td>AAA</td><td>100</td><td>99</td><td>99%</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
		<div class="row">
			<div class="col-md-6">
				<table class="TB_bulletin table-striped">
					<caption>Dep3</caption>
					<thead>
						<tr>
							<th>機種</th><th>計劃數量</th><th>目前進度</th><th>完成度</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>AAA</td><td>100</td><td>99</td><td>99%</td>
						</tr>
						<tr>
							<td>BBB</td><td>200</td><td>100</td><td>50%</td>
						</tr>
						<tr>
							<td>AAA</td><td>100</td><td>99</td><td>99%</td>
						</tr>
						<tr>
							<td>BBB</td><td>200</td><td>100</td><td>50%</td>
						</tr>
						<tr>
							<td>AAA</td><td>100</td><td>99</td><td>99%</td>
						</tr>
					</tbody>
				</table>
			</div>
			<div class="col-md-6">
				<table class="TB_bulletin table-striped">
					<caption>Dep4</caption>
					<thead>
						<tr>
							<th>機種</th><th>計劃數量</th><th>目前進度</th><th>完成度</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>AAA</td><td>100</td><td>99</td><td>99%</td>
						</tr>
						<tr>
							<td>BBB</td><td>200</td><td>100</td><td>50%</td>
						</tr>
						<tr>
							<td>AAA</td><td>100</td><td>99</td><td>99%</td>
						</tr>
						<tr>
							<td>BBB</td><td>200</td><td>100</td><td>50%</td>
						</tr>
						<tr>
							<td>AAA</td><td>100</td><td>99</td><td>99%</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
		<div class="row">
			<div class="col-md-12">
				<h3 class="marquee"><marquee>宣導事項1 .....宣導事項1 .....</marquee></h3>
			</div>
		</div>
	</div>
</div>
</body>
</html>