import os
from pathlib import Path


def get_data_directory() -> Path:
    configured_directory = os.environ.get("CALORIE_TRACKER_DATA_DIR")
    if configured_directory:
        directory = Path(configured_directory).expanduser().resolve()
    else:
        local_app_data = os.environ.get("LOCALAPPDATA")
        if not local_app_data:
            raise RuntimeError("LOCALAPPDATA is required for the Windows data directory.")
        directory = Path(local_app_data) / "CalorieTracker"

    directory.mkdir(parents=True, exist_ok=True)
    return directory


def get_database_path() -> Path:
    return get_data_directory() / "tracker.sqlite3"