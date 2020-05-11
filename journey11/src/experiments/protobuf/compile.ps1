# conda activate notebook_gpu_netx
# make sure conda\bin conda\scripts are on the system file path
#
. ..\..\..\..\ps1\ProtoComplie.ps1

$local = "d:/Dev/devroot/AI-Intuition/journey11/src/experiments/protobuf"
$rmt = "/var/data"

ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename addressbook.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename complex.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename helloworld.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename state.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename task.proto

