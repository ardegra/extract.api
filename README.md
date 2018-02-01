# Extract API
Extract API is REST API that can crawl a website. You can make use of this API to crawl a website such as News and Forum.

To use this Extract API, you need to have `MongoDB` installed and `Python 3`. In this case, we assume that you already have those 2.

## Installation
  1. `pip install -r requirements.txt`
  2. `gunicorn run:api -b 0.0.0.0:8000 --reload`

## Configuration
The configuration of this Extract API is located in `lib/config.py`. Please only modify that file, do not modify anything unless you understand the risk.