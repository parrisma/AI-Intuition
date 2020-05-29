param (
    [String]$ComposeYML = "./docker-compose-ai.yml",
    [String]$StackName = "ai",
    [Switch]$StopOnly
)

. ..\..\ps1\BuildDockerFile.ps1

if (DockerIsSwarmManager)
{
    Write-Output "Local Host is Swarm Manager: OK"
}
else
{
    Write-Error "Docker daemon must be manager to run this swarm"
    Write-Error "run Docker init swarm"
    exit
}

# docker-compose-ai.yml has start constraints based on Labels, so add the labels below
# if not already added to the docker daemon.
#
# docker node inspect docker-desktop --format '{{.Spec.Labels}}'
#
# docker node update --label-add kafka=true docker-desktop
# docker node update --label-add zookeeper=true docker-desktop

DockerStartStack -StackName $StackName -ComposeYML $ComposeYML