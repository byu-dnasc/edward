from fastapi.testclient import TestClient
import pytest
from sqlmodel import create_engine, StaticPool, Session, SQLModel
from unittest.mock import MagicMock, patch

from app.endpoints import FASTAPI
from app import smrtlink
from app.database import Dataset, get_session
from app.filesystem import StagingException

class TestProject(smrtlink.Project):
    def __init__(self, id: int, datasets: dict[str, dict]):
        self._id = id
        self._datasets = datasets

client = TestClient(FASTAPI)

DATASET_CONSTRUCTOR = 1
STAGE = 2
UNDO_STAGING = 3

mock_dataset = MagicMock()
mock_dataset.dir_path = ''

patchers = {
    DATASET_CONSTRUCTOR: patch('app.collection.Dataset', return_value=mock_dataset),
    STAGE: patch('app.filesystem.stage', return_value=''),
    UNDO_STAGING: patch('app.filesystem.delete_dir'),
}

@pytest.fixture
def mock():
    '''
    Require this fixture to override behavior of all those functions `patch`ed in `patchers`.
    '''
    mocks = {i: patcher.start() for i, patcher in patchers.items()}
    yield mocks
    patch.stopall()

@pytest.fixture(name="session")  
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(autouse=True)
def override_get_session(session: Session):
    FASTAPI.dependency_overrides[get_session] = lambda: session

@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    FASTAPI.dependency_overrides.clear()

def override_smrtlink_project(id: int, datasets: dict[str, dict]):
    project = TestProject(id=id, datasets=datasets)
    FASTAPI.dependency_overrides[smrtlink.Project] = lambda: project

def test_post_sanity():
    override_smrtlink_project(id=2, datasets={})
    response = client.post("/smrt-link/projects")
    assert response.status_code == 200

def test_post_insert_database(session: Session, mock):
    uuid = 'a'
    override_smrtlink_project(id=2, datasets={uuid: {}})
    response = client.post("/smrt-link/projects")
    assert response.status_code == 200
    assert session.get_one(Dataset, uuid)

def test_post_stolen_dataset(session: Session):
    uuid = 'a'
    project_before = 2
    session.add(Dataset(uuid=uuid, project_id=project_before, dir_path=''))
    session.commit()
    project_after = 3
    override_smrtlink_project(id=project_after, datasets={uuid: {}})
    response = client.post("/smrt-link/projects")
    assert response.status_code == 200
    assert session.get_one(Dataset, uuid).project_id == project_after

def test_post_stage(mock):
    override_smrtlink_project(id=2, datasets={'a': {}})
    response = client.post("/smrt-link/projects")
    assert response.status_code == 200
    mock[STAGE].assert_called_once()

def test_post_undo_staging(mock):
    override_smrtlink_project(id=2, datasets={'a': {}})
    mock[STAGE].side_effect = StagingException
    response = client.post("/smrt-link/projects")
    assert response.status_code == 200
    mock[UNDO_STAGING].assert_called_once()
