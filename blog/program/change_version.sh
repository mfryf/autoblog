if [ $# != 1 ];then
        echo USAGE:$0 new_version
        exit 1
fi
new_version=$1
version=`cat version`
cat mengfanrong/csdnblog_publish.py|sed "s;version=\"$version\";version=\"$new_version\";g">tmp.py
cp tmp.py mengfanrong/csdnblog_publish.py
./bat_generate.sh
rm tmp.py
echo "version:"`cat version`
