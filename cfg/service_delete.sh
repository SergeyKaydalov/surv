
if [ x$1 = x ]; then
	echo "Usage: service_init.sh <node>"
        echo "     <node> is aggr or mec1"
	exit 0
fi

node=$1
path=$(pwd)/$node

if [ ! -d $path ]; then
	echo "Unknown service $path" && exit 1
fi


kubectl delete -f $path/services.yaml
kubectl delete -f $path/cluster.yaml


 
