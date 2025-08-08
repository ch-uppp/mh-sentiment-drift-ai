# Deployment Commands
## Apply namespace first
kubectl apply -f namespace.yaml

##  Apply all configurations
kubectl apply -f configmaps/
kubectl apply -f persistent-volumes/
kubectl apply -f deployments/
kubectl apply -f services/

## Check deployment status
kubectl get all -n sentiment-drift

## View logs
kubectl logs -f deployment/sentiment-analysis-deployment -n sentiment-drift

## Scale deployment
kubectl scale deployment sentiment-analysis-deployment --replicas=5 -n sentiment-drift
