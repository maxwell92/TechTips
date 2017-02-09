PID="./ycepid"
function test_exit(){
	pid=""
	if [ -f $PID ] ;then
	    pid=`cat $PID`
	fi
	
	pid_cur=`pgrep -l yce|cut -d " " -f 1`
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

re=`test_exit`
echo $re
