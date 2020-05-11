Function ProtoCompile
{
    [cmdletbinding()]
    Param (
        [string]$Filename,
        [string]$LocalDir,
        [string]$ConatinerDir
    )
    Process {
        Write-Output "Compiling : [$Filename]"
        docker run -it -v $LocalDir"":$ConatinerDir parrisma/py-env:1.0 protoc --proto_path=$ConatinerDir --python_out=$ConatinerDir $ConatinerDir/$Filename
        Write-Output "Done"
    }
}