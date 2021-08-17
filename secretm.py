from google.cloud import secretmanager

class Secretm():
    def __init__(self, project):
        self.project = project
        self.client = secretmanager.SecretManagerServiceClient()

    def get(self, secret_id, version_id="latest"):
        project_id = self.project
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return payload
