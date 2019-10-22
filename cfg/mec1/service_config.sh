#
# Create a NFS share and 2 ISGW sender services
# To be executed inside a target pod of a MEC server
#

export NEDGE_HOME=/opt/nedge

source /opt/nedge/env.sh

# create cluster, tenant and buckets
efscli system init -f
efscli cluster create sfo
efscli tenant create sfo/terminal1
efscli bucket create sfo/terminal1/video -s 128k
efscli bucket create sfo/terminal1/capture -s 128k

# create a NFS service on a MEC device to store video and pictures
efscli service create nfs nfs-mec1
efscli service config nfsmec1 X-MH-ImmDir 1
efscli service serve nfs-mec1 sfo/terminal1/video
efscli service serve nfs-mec1 sfo/terminal1/capture

# An inter-sergement link with metadata-only replication for videos
efscli service create isgw isgw-stream
efscli service serve isgw-stream sfo/terminal1/video                                     
efscli service config isgw-stream X-Status enabled                                   
efscli service config isgw-stream X-ISGW-Replication 3                               
efscli service config isgw-stream X-ISGW-MDOnly 2                                    
efscli service config isgw-stream X-ISGW-Direction 3                                 

# An inter-sergement link with full replication for pictures
efscli service create isgw isgw-capture
efscli service serve isgw-capture sfo/terminal1/capture                                      
efscli service config isgw-capture X-Status enabled                                   
efscli service config isgw-capture X-ISGW-Replication 3                               
efscli service config isgw-capture X-ISGW-Direction 3                                 
