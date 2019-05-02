# rio-tiler-glob

A custom tile server for dataset stored as band per file

# Usage
Pass a glob url to the tiler e.g: `https://s3.eu-central-1.amazonaws.com/remotepixel-eu-central-1/sentinel-s2-l1c/tiles/18/T/VQ/2019/4/29/0/B0{4,3,2}.tif`

see https://observablehq.com/@vincentsarago/ottawa_gatineau_flood_sentinel2

# Deployment

### Build Docker image

```bash
$ docker-compose build
```

### Create Lambda package

```bash
$ docker-compose run --rm package
```

### Deploy to AWS
```
$ brew install terraform

# Set ${AWS_ACCESS_KEY_ID} and ${AWS_SECRET_ACCESS_KEY} in your env
$ terraform init
$ terraform apply --var bucket={additional bucket to grant access to} --var region=us-west-2
```


## Debug

edit [bin/test.sh](bin/test.sh)

```bash
# Create package
$ docker-compose build
$ docker-compose run --rm package

# test services
$ docker-compose run --rm test
```