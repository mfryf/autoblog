if [ $# != 1 ] && [ $# != 2 ];then
    echo "USAGE:$0 username [isShow(true)]"
	exit 1
fi
username=$1
isShow=${2-true}
if [ -d $username ];then
    rm $username -r
fi
if [ "$username" = "mengfanrong" ];then
    echo username should not be mengfanrong
	exit 1
fi
cat mengfanrong/csdnblog_publish.py|sed "s;'python csdnblog_publish.py';'pythonw csdnblog_publish.pyw';g"> mengfanrong/csdnblog_publish.pyw
#rm temp files
if [ -f mengfanrong/html.zip ];then
	rm mengfanrong/html.zip
fi
if [ -f mengfanrong/similiar.txt ];then
	rm mengfanrong/similiar.txt
fi
if [ -f mengfanrong/csdnblog_publish.py.lnk ];then
	rm mengfanrong/csdnblog_publish.py.lnk
fi

if [ -f mengfanrong/bat_replace.pyc ];then
	rm mengfanrong/bat_replace.pyc
fi

cat mengfanrong/csdnblog_publish.py|grep "version=\""|awk -F '"' '{print $2}'>version
mkdir -p $username
cp mengfanrong/*  $username/ -r

for file in `find $username -type f`
do
    cat $file|sed "s;mengfanrong;$username;g" >$file.tmp
	mv $file.tmp $file
done
if [ "$isShow" = "false" ];then
	cat $username/install.bat|sed "s;csdnblog_publish.py\";csdnblog_publish.pyw\";g">$username/install.bat.tmp
	mv $username/install.bat.tmp $username/install.bat
fi
echo finish $username
