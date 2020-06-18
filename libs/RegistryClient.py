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
        response = requests.get(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_name}")
        tag_manifest = json.loads(response.content.decode('utf-8'))
        return json.loads(tag_manifest["history"][0]["v1Compatibility"])["created"]

    def delete_tag(self, repository, tag_name):
        response = requests.get(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_name}")
        tag_digest = json.loads(response.content.decode('utf-8'))["fsLayers"][0]["blobSum"]
        response = requests.get(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_name}", headers={"Authorization": "Basic <" + tag_digest + ">", "Accept": "application/vnd.docker.distribution.manifest.v2+json"})
        tag_content_digest = response.headers["Docker-Content-Digest"]
        response = requests.delete(f"{self.API_ENDPOINT}/{repository}/manifests/{tag_content_digest}")
        if response.status_code == 202:
            return f"{tag_name} from repository: '{repository}' was deleted."

    def search_tag(self, repository, tag_like=None, tag_time=None, tag_keep=None):
        result = {}
        all_tags = self.repository_tags(repository)
        tmp = [tag for tag in all_tags]
        for tag_name in tmp:
            result[tag_name] = self.tag_creation_time(repository, tag_name)

        if (tag_like or tag_time or tag_keep) is None:
            return result
        else:
            if tag_like is None:
                pass
            else:
                result = {key: value for (key, value) in result.items() if tag_like in key}
            if tag_time is None:
                pass
            else:
                tmp = {}
                for key in result:
                    if tag_time > result[key][0:19]:
                        tmp[key] = result[key][0:19]
                result = tmp
            if tag_keep is None:
                pass
            else:
                tmp = {}
                sorted_not_to_keep = sorted(result.items(), key=lambda x: x[1], reverse=True)[tag_keep:]
                for tag in sorted_not_to_keep:
                    tmp[tag[0]] = tag[1]
                result = tmp
            return result

    def purge_repository(self, repository):
        for tag_name in self.repository_tags(repository):
            self.delete_tag(repository, tag_name)

    def purge_registry(self):
        for repository in self.repositories():
            self.purge_repository(repository)
