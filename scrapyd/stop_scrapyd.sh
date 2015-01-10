#

pid=$(cat twistd.pid)
echo "$pid"
kill $pid
