./generate_one_program.sh blfshiye
./generate_one_program.sh gcczhongduan
./generate_one_program.sh hrhguanli
./generate_one_program.sh lcchuguo
./generate_one_program.sh mfrbuaa
./generate_one_program.sh mfryf
./generate_one_program.sh phlsheji
./generate_one_program.sh yxwkaifa
./generate_one_program.sh zfyouxi
for file in `find ./ -name "*.bat"`
do
    sed -e 's/$/\r/' $file > $file.tmp
    mv $file.tmp $file
done
