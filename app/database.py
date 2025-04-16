from datetime import datetime
from typing import Annotated
import fastapi
import sqlmodel
import app

class Dataset(sqlmodel.SQLModel, table=True):
    uuid: str = sqlmodel.Field(primary_key=True)
    project_id: int
    dir_path: str

def dataset_update_project(datasets: list[str], project_id: int):
    '''
    `datasets`: a list of dataset uuids. This query will update the `project_id`
    of datasets whose uuid is among this list.
    '''
    return (sqlmodel.update(Dataset)
                    .where(Dataset.uuid.in_(datasets))
                    .values(project_id=project_id))

def get_stolen_datasets(new_project_datasets: list[str]) -> list[str]:
    return sqlmodel.select(Dataset.uuid).where(Dataset.uuid.in_(new_project_datasets))

def get_datasets_by_project(project_id: int):
    return sqlmodel.select(Dataset).where(Dataset.project_id == project_id)
    
class AccessRule(sqlmodel.SQLModel, table=True):
    id: str = sqlmodel.Field(primary_key=True)
    project_id: int
    user_id: str
    dataset_uuid: str
    expiry: datetime

engine = sqlmodel.create_engine(
    url="sqlite://" if app.DB_PATH == "" else f"sqlite:///{app.DB_PATH}",
    connect_args={"check_same_thread": False},
    poolclass=sqlmodel.StaticPool
)

def create_tables():
    sqlmodel.SQLModel.metadata.create_all(engine)

def get_session():
    with sqlmodel.Session(engine) as session:
        yield session

SessionDep = Annotated[sqlmodel.Session, fastapi.Depends(get_session)]

class Project(app.BaseProject):
    def __init__(self, id: int, session: SessionDep):
        dataset_uuids = session.exec(
            sqlmodel.select(Dataset.uuid).where(Dataset.project_id == id)
        ).all()
        self._id = id
        self._datasets = set(dataset_uuids)
        self._members = ... # TODO

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def datasets(self) -> set[str]:
        return self._datasets
    
    @property
    def members(self) -> set[str]:
        return self._members

if __name__ == '__main__':
    create_tables()
else:
    pass # tables are created elsewhere