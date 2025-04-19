resource kv 'Microsoft.KeyVault/vaults@2023-04-01' = {
  name: 'erynKeyVault'
  location: resourceGroup().location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    accessPolicies: []
    enabledForDeployment: true
    enabledForTemplateDeployment: true
    enabledForDiskEncryption: true
  }
}
