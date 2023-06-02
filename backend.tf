terraform {
  backend "remote" {
    organization = "cloudfelipe"

    workspaces {
      name = "cna-01"
    }
  }
}