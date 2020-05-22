import json
import requests


class RegistryClient:
    def __init__(self, api_url, api_version):
        self.API_ENDPOINT = f"http://{api_url}/{api_version}/"

    def configuration(self):
        return self.API_ENDPOINT

    def repositories(self):
        response = requests.get(f"{self.API_ENDPOINT}_catalog")
        return response.json()['repositories']

    def repository_tags(self, repository):
        response = requests.get(f"{self.API_ENDPOINT}/{repository}/tags/list")
        return response.json()['tags']

    def delete_tag_id(self, repository, tag_id):
        response = requests.get(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_id}")
        tag_digest = json.loads(response.content.decode('utf-8'))["fsLayers"][0]["blobSum"]
        response = requests.get(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_id}", headers={"Authorization": "Basic <" + tag_digest + ">", "Accept": "application/vnd.docker.distribution.manifest.v2+json"})
        tag_content_digest = response.headers["Docker-Content-Digest"]
        response = requests.delete(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_content_digest}")
        if response.status_code == 202:
            return f"{tag_id} from repository: '{repository}' was deleted."

    def delete_tag_time(self):
        pass

    def purge_repository(self):
        pass

    def cleanup(self):
        pass