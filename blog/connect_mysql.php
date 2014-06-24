<?php
	/************存入数据库****************/
	//建立连接
	$con = mysql_pconnect("10.0.16.16:4066","QQNyqcfO","17WhjmVARGf2");
	mysql_query("set names utf8");
	if (!$con)
	{
	  write_log('Could not connect: ' . mysql_error());
	  die('Could not connect: ' . mysql_error());	  
	}
	//选择数据库
	mysql_select_db("3811608500p_mysql_w6nyu5ot", $con);
?>