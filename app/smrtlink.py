import urllib3
from requests.exceptions import HTTPError

import app.smrtlink_client
import app

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DnascSmrtLinkClient(app.smrtlink_client.SmrtLinkClient):

    def get_project(self, id: int) -> dict:
        '''
        Returns a dictionary of project data, or None if not found.
        '''
        try:
            return self.get(f"/smrt-link/projects/{id}")
        except HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise Exception(f'Error getting data from SMRT Link: {e}')
    
    def get_project_ids(self) -> list[int]:
        '''
        Returns the ids of all projects in SMRT Link.
        '''
        lst = self.get("/smrt-link/projects")
        return [dct['id'] for dct in lst]
   
try:
    CLIENT = DnascSmrtLinkClient(
        host=app.SMRTLINK_HOST,
        port=app.SMRTLINK_PORT,
        username=app.SMRTLINK_USER,
        password=app.SMRTLINK_PASS,
        verify=False # Disable SSL verification
    )
except Exception as e:
    CLIENT = None 
    # app.logger.error(f'Error initializing SMRT Link client: {e}')

def _get_project(project_id: int):
    return CLIENT.get_project(project_id)

def _get_new_project():
    project_id = CLIENT.get_project_ids()[-1]
    return CLIENT.get_project(project_id)

class Project:

    def __init__(self, project_id: int = 0):
        '''
        `project_id`: the id of the project to get from SMRT Link. Note that when
        this function is a dependency of a FastAPI project endpoint that has `project_id`
        as a path parameter, then FastAPI will pass the project_id to this function.
        '''
        if project_id == 0:
            project = _get_new_project()
        else:
            project = _get_project(project_id)
        self._id = project_id
        self._datasets = {metadata['uuid']: metadata for metadata in project['datasets']}
        self._members = set()
    
    @property
    def datasets(self) -> dict[str, dict]:
        return self._datasets
    
    @property
    def id(self) -> int:
        return self._id