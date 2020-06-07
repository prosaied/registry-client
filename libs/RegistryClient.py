import json
import requests


class RegistryClient:
    def __init__(self, api_url, api_version):
        self.API_ENDPOINT = f"http://{api_url}/{api_version}/"

    def show_configuration(self):
        return self.API_ENDPOINT

    def repositories(self):
        response = requests.get(f"{self.API_ENDPOINT}_catalog")
        return response.json()['repositories']

    def repository_tags(self, repository):
        response = requests.get(f"{self.API_ENDPOINT}/{repository}/tags/list")
        return response.json()['tags']

    def tag_detail(self, repository, tag_name):
        response = requests.get(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_name}")
        return json.dumps(response.json(), indent=2)

    def tag_creation_time(self, repository, tag_name):
        pass

    def delete_tag(self, repository, tag_name):
        response = requests.get(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_name}")
        tag_digest = json.loads(response.content.decode('utf-8'))["fsLayers"][0]["blobSum"]
        response = requests.get(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_name}", headers={"Authorization": "Basic <" + tag_digest + ">", "Accept": "application/vnd.docker.distribution.manifest.v2+json"})
        tag_content_digest = response.headers["Docker-Content-Digest"]
        response = requests.delete(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_content_digest}")
        if response.status_code == 202:
            return f"{tag_name} from repository: '{repository}' was deleted."

    def search_tag(self, repository, tags_like):
        all_tags = self.repository_tags(repository)
        expression_result = [tag for tag in all_tags if tags_like in tag]
        return expression_result

    def purge_repository(self, repository):
        for tag_name in self.repository_tags(repository):
            self.delete_tag(repository, tag_name)

    def purge_registry(self):
        for repository in self.repositories():
            self.purge_repository(repository)
