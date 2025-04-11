import pwd
import os

import app.collection
import app

os.umask(0) # allow permissions to be specified explicitly
DIR_PERMISSION=0o1775 # allow group to add and remove their own files, but not delete the directory

class StagingException(Exception):
    ...

try:
    if not os.path.exists(app.STAGING_ROOT):
        os.mkdir(app.STAGING_ROOT, DIR_PERMISSION)
except Exception as e:
    print(f"Failed to create staging root directory: {e}")

def _make_dir(dir):
    path = os.path.join(app.STAGING_ROOT, dir)
    os.makedirs(path,
             DIR_PERMISSION, 
             exist_ok=True)
    return path

def stage(collection: app.collection.FileCollection) -> str:
    '''
    Creates a directory and populates it with links to files belonging to the `collection`.
    Directory is a subdirectory of app.STAGING_ROOT if `collection is Dataset` is True.
    Otherwise, the new directory will be a sub-subdirectory of app.STAGING_ROOT.

    Returns the path of the new directory it creates.

    Raises StagingException if anything goes wrong, usually a filesystem exception.
    '''
    try:
        dir = _make_dir(collection.dir_path)
        for filepath in collection.files:
            os.link(filepath, os.path.join(app.STAGING_ROOT, dir, os.path.basename(filepath)))
        return dir
    except Exception as e:
        raise StagingException

def _get_user(filepath):
    return pwd.getpwuid(os.stat(filepath).st_uid).pw_name

def delete_dir(path):
    if not os.path.exists(path):
        return
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            fileowner = _get_user(filepath)
            if fileowner == app.APP_USER:
                os.remove(filepath)
    os.rmdir(path)
