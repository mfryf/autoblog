if [ $# != 1 ];then
    echo USAGE:$0 username
	exit 1
fi
username=$1
if [ -d $username ];then
    rm $username -r
fi
if [ "$username" = "mengfanrong" ];then
    echo username should not be mengfanrong
	exit 1
fi
cp mengfanrong/csdnblog_publish.py mengfanrong/csdnblog_publish.pyw
rm mengfanrong/html.zip mengfanrong/similiar.txt mengfanrong/csdnblog_publish.py.lnk
cat mengfanrong/csdnblog_publish.py|grep "version=\""|awk -F '"' '{print $2}'>version
mkdir -p $username
cp mengfanrong/*  $username/ -r
cat $username/csdnblog_publish.pyw|sed "s;mengfanrong;$username;g">$username/csdnblog_publish.pyw.tmp
mv $username/csdnblog_publish.pyw.tmp $username/csdnblog_publish.pyw
cat $username/csdnblog_publish.py|sed "s;mengfanrong;$username;g">$username/csdnblog_publish.py.tmp
mv $username/csdnblog_publish.py.tmp $username/csdnblog_publish.py
