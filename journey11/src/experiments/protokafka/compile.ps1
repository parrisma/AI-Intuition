# conda activate notebook_gpu_netx
# make sure conda\bin conda\scripts are on the system file path
#
. ..\..\..\..\ps1\ProtoComplie.ps1

$local = "d:/Dev/devroot/AI-Intuition/journey11/src/experiments/protokafka"
$rmt = "/var/data"

ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename state.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename pb_task.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename message1.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename message2.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename message3.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename notification.proto

