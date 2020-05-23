Function RunPyEnv
{
    [cmdletbinding()]
    Param (
        [string]$Filename,
        [string]$LocalDir,
        [string]$ConatinerDir
    )
    Process {
        Write-Output "Compiling : [$Filename]"
        docker run -v $LocalDir"":$ConatinerDir parrisma/pyenv:1.0
        Write-Output "Done"
    }
}

$local = "d:/Dev/devroot/AI-Intuition/journey11/src/experiments/protokafka"
$rmt = "/var/data"

RunPyEnv -LocalDir $local -ConatinerDir $rmt -Filename pb_state.proto