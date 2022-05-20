################################################################################
# Providers
################################################################################

terraform {
  required_providers {
    heroku = {
      source  = "heroku/heroku"
      version = "~> 5.0"
    }
    herokux = {
      source  = "davidji99/herokux"
      version = "0.33.2"
    }
  }
}


################################################################################
# Input variable definitions
################################################################################

variable "deployment_name" {
  description = "Name of the deployment."
  type        = string
}

variable "image_tag" {
  description = "full image gcr image tag"
  type        = string
}

variable "image_repository" {
  description = "gcr repository name"
  type        = string
}

variable "image_version" {
  description = "gcr image version"
  type        = string
}

variable "region" {

}
variable "dyno_count" {

}

variable "dyno_type" {

}

################################################################################
# Resources
################################################################################

resource "heroku_app" "bento" {
  #todo: append with random string
  name   = "${var.deployment_name}-jjamchan"
  region = "us"
}

data "herokux_registry_image" "img" {
  app_id       = heroku_app.example.uuid
  process_type = "web"
  docker_tag   = "latest"
}

resource "herokux_app_container_release" "release" {
  app_id       = heroku_app.bento.uuid
  image_id     = data.herokux_registry_image.img.digest
  process_type = "web"
}

# Launch the app's web process by scaling-up
resource "heroku_formation" "formation" {
  app_id     = heroku_app.bento.id
  type       = "web"
  quantity   = var.dyno_count
  size       = var.dyno_type
  depends_on = [herokux_app_container_release.release]
}


################################################################################
# Output value definitions
################################################################################

output "example_app_url" {
  value = "https://${heroku_app.bento.name}.herokuapp.com"
}
