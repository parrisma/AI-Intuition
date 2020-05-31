# Compile the ProtoBuf files
#
. ..\..\..\..\ps1\ProtoComplie.ps1

$local = "d:/Dev/devroot/AI-Intuition/journey11/src/lib/kpubsub"
$rmt = "/var/data"
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename pb_notification.proto

