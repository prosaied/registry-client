from libs.RegistryClient import RegistryClient

regclient = RegistryClient('demo-registry.digikala.com', 'v2')
# print(regclient.tag_creation_time('image-cleaner','stable-12'))
print(regclient.search_tag(repository='image-cleaner', tag_like='sta'))

