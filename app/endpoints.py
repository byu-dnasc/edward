from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, APIRouter

from app import smrtlink
from app import database
from app import BaseProject
from app import filesystem
from app import collection

projects_route = APIRouter()

def get_dataset_metadata(project: Annotated[BaseProject, Depends(smrtlink.Project)]):
    return project.datasets

def get_stolen_datasets(
        project: Annotated[BaseProject, Depends(smrtlink.Project)],
        session: database.SessionDep
    ) -> list[str]:
    '''
    Return those datasets found in `project` that belonged to a different
    project as of the last known state recorded in the database.
    '''
    return session.exec(database.get_stolen_datasets(project.datasets.keys())).all()

def get_new_datasets(
        project: Annotated[BaseProject, Depends(smrtlink.Project)], 
        stolen_datasets: Annotated[list[str], Depends(get_stolen_datasets)]
    ) -> list[str]:
    '''
    Return those datasets found in `project` that are not found in the database.
    If the app is up to date on projects, this will effectually identify those datasets
    that are new to the project which also belonged previously to no other project 
    other than the general project.
    '''
    return [d for d in project.datasets.keys() if d not in stolen_datasets]

def get_project_id(project: Annotated[BaseProject, Depends(smrtlink.Project)]) -> int:
    return project.id

@projects_route.post("")
async def new_project(
    dataset_metadata: Annotated[dict[str, dict], Depends(get_dataset_metadata)],
    stolen_datasets: Annotated[list[str], Depends(get_stolen_datasets)],
    new_datasets: Annotated[list[str], Depends(get_new_datasets)],
    project_id: Annotated[int, Depends(get_project_id)],
    session: database.SessionDep
):
    # update the project id of the stolen datasets in the database
    session.exec(database.dataset_update_project(stolen_datasets, project_id))
    session.commit()
    # stage the new datasets
    directories = {}
    for uuid in new_datasets:
        dataset = collection.Dataset(**dataset_metadata[uuid])
        try:
            directories[uuid] = filesystem.stage(dataset)
        except filesystem.StagingException:
            # log exception
            # clean up any partial staging results
            filesystem.delete_dir(dataset.dir_path)
    # create a record of each dataset that was staged
    staged_datasets = [
        database.Dataset(uuid=uuid, project_id=project_id, dir_path=dir_path)
        for uuid, dir_path in directories.items()
    ]
    # insert these records in the database
    session.add_all(staged_datasets)
    session.commit()

def get_datasets_by_project(project_id: int, session: database.SessionDep) -> list[database.Dataset]:
    return list(session.exec(database.get_datasets_by_project(project_id)).all())

LastKnownDatasetsDep = Annotated[list[database.Dataset], Depends(get_datasets_by_project)]

def get_removed_datasets(
    project: Annotated[BaseProject, Depends(smrtlink.Project)],
    last_known_datasets: LastKnownDatasetsDep
) -> list[database.Dataset]:
    '''
    Return those datasets that are not found in the project but belonged to it last time
    the app received an update.
    '''
    return [d for d in last_known_datasets if d.uuid not in project.datasets.keys()]

@projects_route.put("/{project_id}")
async def update_project(
    dataset_metadata: Annotated[dict[str, dict], Depends(get_dataset_metadata)],
    removed_datasets: Annotated[list[database.Dataset], Depends(get_removed_datasets)],
    stolen_datasets: Annotated[list[str], Depends(get_stolen_datasets)],
    new_datasets: Annotated[list[str], Depends(get_new_datasets)],
    project_id,
    session: database.SessionDep
):
    '''
    Same as `new_project`, plus handling of `removed_datasets`. TODO: De-duplicate?
    The only other difference is that `project_id` is a path parameter, which will alter
    the behavior of `smrtlink.Project`.
    '''
    # undo staging of datasets that no longer belong to this project
    for dataset in removed_datasets:
        filesystem.delete_dir(dataset.dir_path)
        session.delete(dataset)
    # update the project id of the stolen datasets in the database
    session.exec(database.dataset_update_project(stolen_datasets, project_id))
    session.commit()
    # stage the new datasets
    directories = {}
    for uuid in new_datasets:
        dataset = collection.Dataset(**dataset_metadata[uuid])
        try:
            directories[uuid] = filesystem.stage(dataset)
        except filesystem.StagingException:
            # log exception
            # clean up any partial staging results
            filesystem.delete_dir(dataset.dir_path)
    # create a record of each dataset that was staged
    staged_datasets = [
        database.Dataset(uuid=uuid, project_id=project_id, dir_path=dir_path)
        for uuid, dir_path in directories.items()
    ]
    # insert these records in the database
    session.add_all(staged_datasets)
    session.commit()

@projects_route.delete("/{project_id}")
async def delete_project(project_datasets: LastKnownDatasetsDep, session: database.SessionDep):
    for dataset in project_datasets:
        # undo staging of this project's datasets
        filesystem.delete_dir(dataset.dir_path)
        # remove records of these datasets from the database
        session.delete(dataset)
        session.commit()

def smrtlink_online():
    # Replace this with the actual implementation to check if SMRT Link is online
    if False:
        raise Exception("SMRT Link is not available")

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
    Ensure tables are created.
    '''
    database.create_tables()

FASTAPI = FastAPI(lifespan=lifespan)
FASTAPI.include_router(
    projects_route,
    prefix="/smrt-link/projects",
    dependencies=[Depends(smrtlink_online)]
)
