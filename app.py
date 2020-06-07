from libs.RegistryClient import RegistryClient

regclient = RegistryClient('demo-registry.digikala.com', 'v2')

print(regclient.search_tag('image-cleaner',))

