# Compile the ProtoBuf files
#
. ..\..\..\..\ps1\ProtoComplie.ps1

$local = "d:/Dev/devroot/AI-Intuition/journey11/src/test/kpubsub"
$rmt = "/var/data"
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename pb_message1.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename pb_message2.proto

