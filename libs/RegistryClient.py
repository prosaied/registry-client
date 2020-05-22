class RegistryClient:
    def __init__(self, api_url, api_version):
        self.API_ENDPOINT = f"http://{api_url}/{api_version}/"

    def show_configuration(self):
        print(self.API_ENDPOINT)

    def show_repositories(self):
        pass

    def show_repository_tags(self):
        pass

    def delete_tag_id(self):
        pass

    def delete_tag_time(self):
        pass

    def purge_repository(self):
        pass

    def cleanup(self):
        pass
