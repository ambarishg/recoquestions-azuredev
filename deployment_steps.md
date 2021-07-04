# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

sudo chmod 666 /var/run/docker.sock

# Build the docker image        
docker build -t reco .   

# Run Docker     
docker run -p 8501:8501 reco

# Login into the Azure Container Registry    
docker tag reco:latest recoacr.azurecr.io/reco:v1  

# Create a Resource Group          
az group create --location centralindia --resource-group recogroup 

# Create a Azure Container Registry    
az acr create --resource-group recogroup --name recoacr --sku Basic 

# Login into the Azure Container Registry     
az acr login -n recoacr   


# Push image into Azure Container Registry  
docker push recoacr.azurecr.io/reco:v1

# Update the  Azure Container Registry 
az acr update -n recoacr --admin-enabled true       

# Get the password of the Azure CLI   
password=$(az acr credential show --name recoacr --query passwords[0].value --output tsv)

# Create the Azure Container        
az container create  --resource-group recogroup  \
--name reco --image recoacr.azurecr.io/reco:v1  \
--registry-login-server recoacr.azurecr.io \
--ip-address Public  --location centralindia  \
--registry-username recoacr \
--registry-password $password  \
--ports 8501 --dns-name-label recoapp --memory 5

# Navigate to http://recoapp.centralindia.azurecontainer.io:8501/




