PID="./ycepid"
function test_exit(){
	pid=""
	if [ -f $PID ] ;then
	    pid=`cat $PID`
	fi
    echo $pid
	
	pid_cur=`pgrep -l yce|cut -d " " -f 1`
    echo $pid_cur
	if [ -n "$pid_cur" ] ;then
	    if [[ "$pid" != "$pid_cur" ]];then
	        echo -n "$pid_cur">$PID 2>/dev/null
	    fi
        echo 0
	    return 0
	else
	    echo -n "">$PID 2>/dev/null
        echo 1
	    return 1
	fi
}

test_exit
