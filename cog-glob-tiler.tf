variable "region" {
  type    = "string"
}
variable "project" {
  description = "The project name"
  default     = "glob-tiler"
}

variable "stage" {
  description = "The stage name(production/staging/etc..)"
  default     = "production"
}

variable "bucket" {
  type    = "string"
}

module "glob" {
  source = "github.com/developmentseed/tf-lambda-proxy-apigw"

  # General options
  project    = "${var.project}"
  stage_name = "${var.stage}"
  region     = "${var.region}"

  # Lambda options
  lambda_name    = "glob"
  lambda_runtime = "python3.6"
  lambda_memory  = 1024
  lambda_timeout = 10
  lambda_package = "package.zip"
  lambda_handler = "rio_tiler_glob.app.APP"

  lambda_env = {
    PYTHONWARNINGS                     = "ignore"
    GDAL_DATA                          = "/var/task/share/gdal"
    GDAL_CACHEMAX                      = "512"
    VSI_CACHE                          = "TRUE"
    VSI_CACHE_SIZE                     = "536870912"
    CPL_TMPDIR                         = "/tmp"
    GDAL_HTTP_MERGE_CONSECUTIVE_RANGES = "YES"
    GDAL_HTTP_MULTIPLEX                = "YES"
    GDAL_HTTP_VERSION                  = "2"
    GDAL_DISABLE_READDIR_ON_OPEN       = "EMPTY_DIR"
    CPL_VSIL_CURL_ALLOWED_EXTENSIONS   = ".tif"
    MAX_THREADS                        = "20"
  }
}

resource "aws_iam_role_policy" "permissions-glob" {
  name = "${module.glob.lambda_role}-bucket-permission"
  role = "${module.glob.lambda_role_id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::${var.bucket}/*"
    }
  ]
}
EOF
}

# Outputs
output "glob_endpoint" {
  description = "Glob dynamic tiler endpoint url"
  value       = "${module.glob.api_url}"
}
