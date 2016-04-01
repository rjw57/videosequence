import contextlib
import hashlib
import logging
import os
import shutil

import pytest
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def _video_fixture_path(name):
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    target_fn = os.path.join(DATA_DIR, name)
    if not os.path.isfile(target_fn):
        raise IOError(("Data file {} not found. "
                       "Have you run test/download_data.sh?").format(name))
    return target_fn

@pytest.fixture
def news_video():
    return _video_fixture_path("news.mp4")

@pytest.fixture
def ice_video():
    return _video_fixture_path("ice.mp4")
