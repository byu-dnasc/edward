class DatasetState:
    dataset_ids = [] # TODO: use set?

    def __init__(self, dataset_ids: list):
        self.dataset_ids = dataset_ids

    def __add__(self, dataset_id: str):
        self.dataset_ids.append(dataset_id)
    
    def __sub__(self, dataset_id: str):
        self.dataset_ids.remove(dataset_id)

DatasetState(["1", "2", "3"]) + "4"
DatasetState(["1", "2", "3"]) - "3"