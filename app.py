from libs.RegistryClient import RegistryClient

regclient = RegistryClient('demo-registry.digikala.com', 'v2')

print(regclient.repositories())
print(regclient.repository_tags('supernova/admin'))
# regclient.delete_tag_id('supernova/admin','nginx-7')
