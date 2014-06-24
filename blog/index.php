<?php
require_once("connect_mysql.php");
require_once("util.php");
if($_SERVER["REQUEST_METHOD"]=="GET")
{
	
	$type = $_GET['type'];
	switch($type)
	{
		case "getOneBlog":
		    getOneBlog();
			break;
		case "updateBlog":
		    updateBlogStateById($_GET['id'],$_GET['user']);
			break;
		default:
			break;
	}
}
function seed()
{
	list($msec, $sec) = explode(' ', microtime());
	return (float) $sec;
}
function updateBlogStateById($id,$user)
{
    $sql="update csdnblog set isPublish=1,published_user='$user' where id=".$id;
	$query=mysql_query($sql);
	$ret=0;
	if( !$query)
	{
		write_log('select failed: ' . mysql_error());
		$ret=-1;	
	}
	echo json_encode(array("ret"=>$ret));
	write_log("updateBlog id:".$id." user:".$user);
}
function getOneBlog()
{
	//查询操作
	$sql="select count(*) from csdnblog where isPublish<>1";
	$query=mysql_query($sql);
	$ret=0;
	if( !$query)
	{
		write_log('select failed: ' . mysql_error());
		$ret=-1;	
	}
	$row=mysql_fetch_array($query);
	$count=$row[0];
	if($count==0)
	{
	    $ret=-1;
		write_log('count is 0');
	}
	srand(seed());
	$start=rand(0,$count-1);
	$sql="select * from csdnblog where isPublish=0 limit ".$start.",1;";
	$query=mysql_query($sql);
	if(!$query)
	{
		write_log('select failed: ' . mysql_error());
		$ret=-1;
	}
	else
	{
		$row=mysql_fetch_array($query); 
		if($row['src_url'] == NULL || $row['src_url'] == '')
		    $ret=-1;
		$list=array("ret"=>$ret,"id"=>$row['id'],"src_url"=>$row['src_url']); 
		echo json_encode($list); 
		write_log("getBlog id:".$row['id'].' src_url:'.$row['src_url']);
	}
}
?>
