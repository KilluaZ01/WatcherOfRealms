import os

def get_persistent_path(filename, subdir=None):
    # Get Windows Local AppData folder, fallback to current dir if env var missing
    base_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'SilverBloodReq')
    if subdir:
        base_dir = os.path.join(base_dir, subdir)
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, filename)