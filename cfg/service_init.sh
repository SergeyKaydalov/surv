
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


kubectl create -f $path/cluster.yaml || (echo "Couldn't create a cluster" && exit 1)
echo Waiting for deployment
sleep 60

kubectl cp $path/service_config.sh rook-edgefs-$node/rook-edgefs-target-0:/root/ -c daemon
kubectl exec -it -n rook-edgefs-$node rook-edgefs-target-0 -c daemon -- bash -c /root/service_config.sh

kubectl create -f $path/services.yaml

 
