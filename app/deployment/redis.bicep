resource redis 'Microsoft.Cache/Redis@2023-04-01' = {
  name: 'erynRedis'
  location: resourceGroup().location
  sku: {
    name: 'Standard'
    family: 'C'
    capacity: 1
  }
  enableNonSslPort: false
  minimumTlsVersion: '1.2'
}
