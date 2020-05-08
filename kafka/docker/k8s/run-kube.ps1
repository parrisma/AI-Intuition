kubectl create namespace ai-intuition
kubectl apply -f .\pods-z-and-k.yml
kubectl delete pod/kafka-pod --namespace ai-intuition
