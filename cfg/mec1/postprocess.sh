
mec_hostname=samsung-kvssd

mec_addr=$(kubectl get nodes -o=wide | grep $mec_hostname | awk '{print $6}')
nfs_ip=$(kubectl get svc -n rook-edgefs-mec1 rook-edgefs-nfs-nfs-mec1 | grep ClusterIP | awk '{print $3}')

echo MEC addr $mec_addr NFS service $nfs_ip

ssh root@$mec_addr "bash -c 'mount $nfs_ip:/mec1/stream /media/stream && mount $nfs_ip:/mec1/capture /media/capture'" && echo "NFS share mounted to /media/stream and /media/capture folders of the MEC1 server"


