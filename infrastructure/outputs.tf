output "resource_group" {
  value = azurerm_resource_group.rg.name
}
output "storage_account" {
  value = azurerm_storage_account.sa.name
}
output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.pg.fqdn
}
