import json
import time
import datetime

from libs.RegistryClient import RegistryClient
import requests

regclient = RegistryClient('demo-registry.digikala.com', 'v2')

# print(regclient.repositories())
# print(regclient.repository_tags('supernova/admin'))
# regclient.delete_tag_id()
# regclient.delete_tag_id('supernova/admin','nginx-7')
# regclient.delete_tag_id('supernova/admin', 'fpm-17')


# response = requests.get('http://demo-registry.digikala.com/v2/supernova/admin/manifests/fpm-17')
# detail = response.json()['history'][0]['v1Compatibility']
# response = response.json.loads(["history"][0]["v1Compatibility"])["created"]

# response = requests.get('http://demo-registry.digikala.com/v2/supernova/admin/tags/list')
# print(response.json()["history"][0]["v1Compatibility"])["created"]

# print(regclient.repositories())
# print(regclient.repository_tags('image-cleaner'))
# print(regclient.tag_detail('image-cleaner', 'stable-3'))

# print(regclient.search_tag('image-cleaner', ''))
# regclient.purge_repository('image-cleaner')

