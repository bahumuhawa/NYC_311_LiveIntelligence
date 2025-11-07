variable "project_name" {
  type        = string
  description = "Short project identifier (e.g., nyc311)"
  default     = "nyc311-intel"
}

variable "location" {
  type        = string
  description = "Azure region"
  default     = "westeurope"
}
