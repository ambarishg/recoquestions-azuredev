# get the current default subscription using show
az account show --output table

# get the current default subscription using list
az account list --query "[?isDefault]"

# get a list of subscriptions except for the default subscription
az account list --query "[?isDefault == \`false\`]"

# get the details of a specific subscription
az account show --subscription "Visual Studio Enterprise Subscription"

az account set --subscription "Visual Studio Enterprise Subscription"