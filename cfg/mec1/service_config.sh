#
# Create a NFS share and 2 ISGW sender services
#

export NEDGE_HOME=/opt/nedge

source /opt/nedge/env.sh

efscli system init -f
efscli cluster create surv
efscli tenant create surv/mec1
efscli bucket create surv/mec1/stream -s 128k
efscli bucket create surv/mec1/capture -s 128k

efscli service create nfs nfs-mec1
efscli service serve nfs-mec1 surv/mec1/stream
efscli service serve nfs-mec1 surv/mec1/capture

efscli service create isgw isgw-stream
efscli service serve isgw-stream surv/mec1/stream                                      
efscli service config isgw-stream X-Status enabled                                   
efscli service config isgw-stream X-ISGW-Replication 3                               
efscli service config isgw-stream X-ISGW-MDOnly 2                                    
efscli service config isgw-stream X-ISGW-Direction 3                                 

efscli service create isgw isgw-capture
efscli service serve isgw-capture surv/mec1/capture                                      
efscli service config isgw-capture X-Status enabled                                   
efscli service config isgw-capture X-ISGW-Replication 3                               
efscli service config isgw-capture X-ISGW-Direction 3                                 
