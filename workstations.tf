resource "google_workstations_cluster" "default" {
  workstation_cluster_id = "trading-cluster"
  location               = "us-central1"
  network                = "default"
  subnetwork             = "default"
}

resource "google_workstations_workstation_config" "default" {
  workstation_config_id = "trading-ide-config"
  location              = "us-central1"
  workstation_cluster_id = google_workstations_cluster.default.workstation_cluster_id

  host {
    gce_instance {
      machine_type                = "e2-standard-4"
      boot_disk_size_gb           = 50
      disable_public_ip_addresses = true
    }
  }

  container {
    image = "us-central1-docker.pkg.dev/cloud-workstations-images/predefined/code-oss:latest"
  }

  persistent_directories {
    mount_path = "/home"
    gce_pd {
      size_gb        = 200
      reclaim_policy = "DELETE"
    }
  }
}

resource "google_workstations_workstation" "default" {
  workstation_id         = "trading-ide"
  location               = "us-central1"
  workstation_cluster_id = google_workstations_cluster.default.workstation_cluster_id
  workstation_config_id  = google_workstations_workstation_config.default.workstation_config_id
}
