from sqlmodel import Session, select, delete
from pytest import fixture

from app.database import Project, Dataset, engine, create_tables

@fixture(autouse=True, scope="function")
def init_db():
    create_tables()
    yield
    Session(engine).exec(delete(Dataset))

def insert(dataset: Dataset):
    with Session(engine) as session:
        session.add(dataset)
        session.commit()

def test_sanity():
    with Session(engine) as session:
        assert session.exec(select(Dataset)).fetchall() == []
    insert(Dataset(uuid="1234", project_id=1, dir_path="/path/to/dataset"))
    with Session(engine) as session:
        assert len(session.exec(select(Dataset)).fetchall()) == 1

def test_project():
    uuid = 'a'
    project_id = 1
    insert(Dataset(uuid=uuid, project_id=project_id, dir_path=""))
    with Session(engine) as session:
        project = Project(project_id, session)
        assert project.datasets == {uuid}