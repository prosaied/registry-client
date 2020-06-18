from libs.RegistryClient import RegistryClient
import click
from pprint import pprint


regclient = RegistryClient('demo-registry.digikala.com', 'v2')



@click.group()
def RegClient():
    """Docker Registry Client Tool"""
    pass


@RegClient.command()
def Show_Configuration():
    print(regclient.show_configuration())


@RegClient.command()
def List_Repositories():
    pprint(regclient.repositories())


@RegClient.command()
@click.option('-r', '--repository', required=True)
def List_Repo_Images(repository):
    print(regclient.repository_tags(repository))


@RegClient.command()
@click.option('-r', '--repository', required=True)
@click.option('-i', '--image_name', required=True)
def Show_Image_Details(repository, image_name):
    print(regclient.tag_detail(repository, image_name))


@RegClient.command()
@click.option('-r', '--repository', required=True)
@click.option('-i', '--image_name', required=True)
def Show_Image_Creation_Time(repository, image_name):
    print(regclient.tag_creation_time(repository, image_name)[0:19])


@RegClient.command()
@click.option('-r', '--repository', required=True)
@click.option('-e', '--image_expression', required=False)
@click.option('-o', '--image_older_than', required=False)
@click.option('-k', '--image_keep_count', required=False)
def Delete_Image(repository, image_expression, image_older_than, image_keep_count):
    print(f"These images are going to be deleted: ")
    images_list = regclient.search_tag(repository, image_expression, image_older_than, image_keep_count)
    pprint(images_list)
    if click.confirm('Do you want to continue?'):
        for image_name in images_list.keys():
            regclient.delete_tag(repository, image_name)


@RegClient.command()
@click.option('-r', '--repository', required=True)
def Purge_Repository(repository):
    print(regclient.purge_repository(repository))


@RegClient.command()
def Purge_Registry():
    regclient.purge_registry()


if __name__ == '__main__':
    RegClient()
