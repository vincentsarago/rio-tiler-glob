#!/bin/bash
python3 -c 'from rio_tiler_glob import __version__ as version; print(version)'


echo "/tilejson.json " && python3 -c 'from rio_tiler_glob.app import APP; resp = APP({"path": "/tilejson.json", "queryStringParameters": {"url": "https://s3.eu-central-1.amazonaws.com/remotepixel-eu-central-1/sentinel-s2-l1c/tiles/18/T/VQ/2019/4/29/0/B0{4,3,2}.tif"}, "pathParameters": "null", "requestContext": "null", "httpMethod": "GET", "headers": {}}, None); print(resp); print("OK") if resp["statusCode"] == 200 else print("NOK")'
echo "/metadata " && python3 -c 'from rio_tiler_glob.app import APP; resp = APP({"path": "/metadata", "queryStringParameters": {"url": "https://s3.eu-central-1.amazonaws.com/remotepixel-eu-central-1/sentinel-s2-l1c/tiles/18/T/VQ/2019/4/29/0/B0{4,3,2}.tif"}, "pathParameters": "null", "requestContext": "null", "httpMethod": "GET", "headers": {}}, None); print(resp); print("OK") if resp["statusCode"] == 200 else print("NOK")'
echo "/tiles " && python3 -c 'from rio_tiler_glob.app import APP; resp = APP({"path": "/10/299/368.png", "queryStringParameters": {"url": "https://s3.eu-central-1.amazonaws.com/remotepixel-eu-central-1/sentinel-s2-l1c/tiles/18/T/VQ/2019/4/29/0/B0{4,3,2}.tif", "rescale": "0,4000"}, "pathParameters": "null", "requestContext": "null", "httpMethod": "GET", "headers": {}}, None); print("OK") if resp["statusCode"] == 200 else print("NOK")'
echo
echo "Done"