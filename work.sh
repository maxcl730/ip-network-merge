begin_with=$1
for ip_range in `cat china_ip_range.txt|grep -v ^#|grep ^$begin_with|awk '{print $1","$2}'`;do
    ip_begin=`echo $ip_range|awk -F ',' '{print $1}'`
    ip_end=`echo $ip_range|awk -F ',' '{print $2}'`
	echo "Querying $ip_begin -- $ip_end >>>>>>>>"
	python ipcalc.py $ip_begin $ip_end
done
