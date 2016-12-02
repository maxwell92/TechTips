for i in `ls`
do
    if [ -d ./$i ]
    then
        rm ./.DS_Store
    fi
    echo "Deleting in "$i
done
echo "Delete Over"
