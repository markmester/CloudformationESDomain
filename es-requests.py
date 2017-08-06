"""
Example of how to sign ES requests when using IAM based auth.
Note that curl doesn't support signed requests.
"""
from elasticsearch import Elasticsearch, RequestsHttpConnection  # pip install elasticsearch
from requests_aws4auth import AWS4Auth  # pip install requests-aws4auth
import os
import re


REGION = 'us-east-1'
HOST = 'search-escluster-2gjz7kw5qd7ueiwkruzjxxsi3q.us-east-1.es.amazonaws.com'

try:
    YOUR_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    YOUR_SECRET_KEY = os.environ['AWS_SECRET_KEY']
except KeyError:
    try:
        with open('/Users/{}/.aws/credentials'.format(os.popen('whoami').read().strip()), 'r') as f:
            out = f.read()
            YOUR_ACCESS_KEY = re.search("aws_access_key_id.*=(.*)", out).group(1).strip()
            YOUR_SECRET_KEY = re.search("aws_secret_access_key.*=(.*)", out).group(1).strip()
    except (IOError, AttributeError) as e:
        raise Exception('Unable to locate AWS credentials', e)


awsauth = AWS4Auth(YOUR_ACCESS_KEY, YOUR_SECRET_KEY, REGION, 'es')

es = Elasticsearch(
    hosts=[{'host': HOST, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.cluster.health())
