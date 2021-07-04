# Install Kubectl - 1
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install Kubectl - 2
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

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

# Get the Service IP External for reco-service e.g.20.193.232.178
kubectl get service

# Navigate to reco-service 
# e.g. <20.193.232.178>:8501 , 20.204.8.140:8501

# Cleanup ( Run in Console)   
az group delete --resource-group recogroup