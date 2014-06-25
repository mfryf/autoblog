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
echo finish $username
