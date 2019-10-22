#
# Create a NFS share and 2 ISGW sender services
# To be executed inside an aggregation pod
#
export NEDGE_HOME=/opt/nedge

source /opt/nedge/env.sh

# Create cluster, tenant and buckets
efscli system init -f
efscli cluster create sfo
efscli tenant create sfo/terminal1
efscli bucket create sfo/terminal1/video -s 128k -t 1
efscli bucket create sfo/terminal1/capture -s 128k -t 1

# Create NFS server to access remote video and captures
efscli service create nfs nfs-aggr
efscli service config nfs-aggr X-MH-ImmDir 1
efscli service serve nfs-aggr sfo/terminal1/video
efscli service serve nfs-aggr sfo/teminal1/capture

# Create an Inter-Segment Link for video streams (on-demand)
efscli service create isgw isgw-stream
efscli service serve isgw-stream sfo/terminal1/video,pause
efscli service config isgw-stream X-Status enabled                                   
efscli service config isgw-stream X-ISGW-Replication 3                               
efscli service config isgw-stream X-ISGW-Direction 3                                 
efscli service config isgw-stream X-ISGW-Basic-Auth None                             

# Create an Inter-Segment Link for captures frames (fully replicated)
efscli service create isgw isgw-capture
efscli service serve isgw-capture sfo/teminal1/capture,pause
efscli service config isgw-capture X-Status enabled                                   
efscli service config isgw-capture X-ISGW-Replication 3                               
efscli service config isgw-capture X-ISGW-Direction 3                                 
efscli service config isgw-capture X-ISGW-Basic-Auth None                             

# Create a S3 gwateway to access remote video and captrures
efscli service create s3 s3-aggr
efscli service serve s3-aggr sfo/terminal1


