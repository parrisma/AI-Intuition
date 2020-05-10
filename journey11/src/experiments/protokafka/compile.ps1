# conda activate notebook_gpu_netx
# make sure conda\bin conda\scripts are on the system file path
#
$local = "//d/Dev/devroot/AI-Intuition/journey11/src/experiments/protokafka"
$rmt = "/var/data"

Function ProtoCompile
{
    [cmdletbinding()]
    Param (
        [string]$Filename,
        [string]$LocalDir,
        [string]$ConatinerDir
    )
    Process {
        echo "Compiling : [$Filename]"
        docker run -it -v $LocalDir"":$ConatinerDir parrisma/py-env:1.0 protoc --proto_path=$ConatinerDir --python_out=$ConatinerDir $ConatinerDir/$Filename
        echo "Done"
    }
}

ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename state.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename task.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename message1.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename message2.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename message3.proto
ProtoCompile -LocalDir $local -ConatinerDir $rmt -Filename notification.proto

