terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.113.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "project_name" {}
variable "location" { default = "westeurope" }

resource "azurerm_resource_group" "rg" {
  name     = "${var.project_name}-rg"
  location = var.location
}

# Storage for raw data
resource "azurerm_storage_account" "sa" {
  name                     = replace(lower("${var.project_name}sa"), "-", "")
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Azure Database for PostgreSQL Flexible Server (skeleton)
resource "azurerm_postgresql_flexible_server" "pg" {
  name                   = "${var.project_name}-pg"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "16"
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
  administrator_login    = "pgadmin"
  administrator_password = "ChangeMeStrong!123"
  zone                   = 1
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.pg.fqdn
}
