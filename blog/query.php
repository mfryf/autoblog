<?php
require_once("connect_mysql.php");
require_once("util.php");
if($_SERVER["REQUEST_METHOD"]=="GET")
{
	
	$type = $_GET['type'];
	switch($type)
	{
		case "getOneBlog":
		    getOneBlog($_GET['username']);
			break;
		case "updateBlog":
		    updateBlogStateById($_GET['id'],$_GET['user'],$_GET['dst_url']);
			break;
		case "addBlog":
		    addOneBlog($_GET['url']);
			break;
		case "getPublishedBlog":
		    getPublishedBlog($_GET['nDaysAgo'],$_GET['cb']);
			break;
		case "updateCookie":
		    updateCookie($_GET['username'],$_GET['cookie']);
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
function addOneBlog($url)
{
    $sql="insert into csdnblog(src_url,create_time) values('$url',now())";
	$query=mysql_query($sql);
	$ret=0;
	if( !$query)
	{
		write_log('insert failed: ' . mysql_error());
		$ret=-1;	
	}
	echo json_encode(array("ret"=>$ret));
}
function updateBlogStateById($id,$user,$dst_url)
{
    $sql="select isPublish from csdnblog where id=".$id;
	$query=mysql_query($sql);
	$row=mysql_fetch_array($query);
	if ($row[0] == 1)
	{
        $ret=-1;
		echo json_encode(array("ret"=>$ret));
		write_log("updateBlog id:".$id." user:".$user."ret:".$ret);
		return;
	}
    $sql="update csdnblog set isPublish=1,published_user='$user',dst_url='$dst_url',update_time=now() where id=".$id;
	$query=mysql_query($sql);
	$ret=0;
	if( !$query)
	{
		write_log('select failed: ' . mysql_error());
		$ret=-1;	
	}
	echo json_encode(array("ret"=>$ret));
	write_log("updateBlog id:".$id." user:".$user."ret:".$ret);
}
function updateCookie($user,$cookie)
{
    $sql="update user_info set cookie='$cookie',update_time=now() where username='$user'";
	$query=mysql_query($sql);
	$ret=0;
	if( !$query)
	{
		write_log('update failed: ' . $sql." ".mysql_error());
		$ret=-1;	
	}
	echo json_encode(array("ret"=>$ret));
}
function getPublishedBlog($nDaysAgo,$cb)
{
    $sql="select published_user,update_time,dst_url,src_url from csdnblog where to_days(update_time)=to_days(now())-$nDaysAgo and isPublish=1  order by update_time desc";
	$query=mysql_query($sql);
	$result=array();
	$index=0;
	while($row=mysql_fetch_array($query))
	{
	    $result[$index]=array("user"=>$row[0],"time"=>$row[1],"dst_url"=>$row[2],"src_url"=>$row[3]);
		$index++;
	}
	$row=mysql_fetch_array(mysql_query("select count(*) from csdnblog"));
	$row2=mysql_fetch_array(mysql_query("select count(*) from csdnblog where isPublish=1"));
	$result[$index]=array("total_blogs"=>$row[0],"published_count"=>$row2[0]);
	echo $cb."(".json_encode($result).")";
}
function getOneBlog($username)
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
		$sql="select cookie from user_info where username='$username'";
		$query=mysql_query($sql);
		if($query)
		{
		    $row_user=mysql_fetch_array($query);
		}
		else
		{
		    $ret=-1;
			write_log("sql failed: " . $sql . mysql_error());
			$row_user['cookie']='failed';
	    }
		$list=array("ret"=>$ret,"id"=>$row['id'],"src_url"=>$row['src_url'],"cookie"=>$row_user['cookie']); 
		echo json_encode($list); 
		write_log("getBlog id:".$row['id'].' src_url:'.$row['src_url']);
	}
}
?>
