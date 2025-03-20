from fastapi import FastAPI, Depends
from typing import Any, Dict, List, Annotated

# FastAPI app instance
app = FastAPI()

def globus_ready():
    # Replace this with the actual implementation to check if Globus is ready
    if False:
        raise GlobusException("Globus is not available")

class SmrtLinkProjectState:
    def __init__(self, project_id: int):
        ... # FIXME: send a request to the smrt-link server to fetch the state
        self.project_id = project_id
        self.datasets = []
        self.members = []

@app.put("/smrt-link/projects/{project_id}", dependencies=[Depends(globus_ready)])
async def update_project(project_state: Annotated[SmrtLinkProjectState, Depends()]):
    return project_state.__dict__

# FastAPI endpoint
@app.post("/smrt-link/projects", dependencies=[Depends(globus_ready)])
async def new_project():
    ...

@app.delete("/smrt-link/projects/{project_id}", dependencies=[Depends(globus_ready)])
async def delete_project(project_id: int):
    ...