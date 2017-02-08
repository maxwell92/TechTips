function yce_status()
{
    ps aux | grep yce | grep -v "grep\|yce" > /dev/null
    return $?
}

if yce_status; then
    echo "yce is running"
    yce_status
    sleep 5
fi

