# Create AKS cluster
az aks create \
    --resource-group recogroup \
    --name recoCluster \
    --node-count 1 \
    --generate-ssh-keys \
    --attach-acr recoacr

# Get AKS cluster credentials
az aks get-credentials --resource-group recogroup --name recoCluster


# Create pods and service 
kubectl apply -f reco.yaml

# Cleanup ( Run in Console)   
az group delete --resource-group recogroup