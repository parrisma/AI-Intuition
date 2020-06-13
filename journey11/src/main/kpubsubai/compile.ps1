# conda activate notebook_gpu_netx
# make sure conda\bin conda\scripts are on the system file path
#
. ..\..\..\..\ps1\ProtoComplie.ps1

$local = "d:/Dev/devroot/AI-Intuition/journey11/src/main/kpubsubai"
$rmt = "/var/data"

ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename pb_uniqueworkref.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename pb_state.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename pb_simplecapability.proto


