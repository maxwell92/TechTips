find . -name "*.woff"
cat > /tmp/prod3
#...ctrl - v...
for i in `cat /tmp/prod3`
do
    echo $i
    dir=`echo $i | cut -d '.' -f 2`
    echo $dir
    mkdir -p fontprod3$dir
    cp $i fontprod3$dir/
done

