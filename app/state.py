import typing
import peewee

class AccessRule(peewee.Model):
    id = peewee.CharField(primary_key=True)
    project_id = peewee.IntegerField()
    user_id = peewee.CharField()
    dataset_uuid = peewee.CharField()
    expiry = peewee.DateTimeField()

    @staticmethod
    def exists(project_id: int, user_id: str) -> bool: # FIXME: doesn't return single result
        return (AccessRule.select()
                            .where(AccessRule.project_id == project_id,
                                   AccessRule.user_id == user_id)
                            .exists())

    @staticmethod
    def get_by_project(project_id: int) -> list['AccessRule']:
        return (AccessRule
                .select()
                .where(AccessRule.project_id == project_id)
                .execute())

    @staticmethod
    def get_one(user_id: str, dataset_id: str) -> typing.Union['AccessRule', None]:
        return AccessRule.get_or_none(AccessRule.user_id == user_id,
                                      AccessRule.dataset_uuid == dataset_id)
    
    @staticmethod
    def get_by_dataset(dataset_id: str) -> list['AccessRule']:
        return (AccessRule.select()
                          .where(AccessRule.dataset_uuid == dataset_id)
                          .execute())
