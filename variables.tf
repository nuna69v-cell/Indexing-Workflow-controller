variable "project_id" {
  description = "The project ID to host the cluster in"
  type        = string
  default     = "your-gcp-project-id"
}

variable "region" {
  description = "The region to host the cluster in"
  type        = string
  default     = "us-central1"
}

variable "zones" {
  description = "The zones to host the cluster in"
  type        = list(string)
  default     = ["us-central1-a", "us-central1-b", "us-central1-c"]
}

variable "cluster_name" {
  description = "The name of the cluster"
  type        = string
  default     = "gke-notebook-cluster"
}

variable "service_account" {
  description = "The service account to use for the nodes"
  type        = string
  default     = ""
}
