import contextlib
import hashlib
import logging
import os
import shutil

import pytest
import requests

CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')

def _video_fixture_filename(url, sha1_hex_digest):
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    target_fn = os.path.join(CACHE_DIR, sha1_hex_digest)

    if not os.path.isfile(target_fn):
        logging.info("Downloading %s", target_fn)
        r = requests.get(url, stream=True)
        content_hash = hashlib.sha1()
        with contextlib.closing(r), open(target_fn, "wb") as fobj:
            r.raise_for_status()
            for chunk in r.iter_content():
                content_hash.update(chunk)
                fobj.write(chunk)
        logging.info("Downloaded content has SHA1: %s", content_hash.hexdigest())
        logging.info("Expexted SHA1: %s", sha1_hex_digest)
        if content_hash.hexdigest() == sha1_hex_digest:
            return target_fn

        shutil.rmtree(target_fn)
        raise RuntimeError("Downloaded data checksum mismatch")
    else:
        logging.info("Skipping existing file %s", url)

    return target_fn

@pytest.fixture
def news_video():
    return _video_fixture_filename(
        "http://www.wim.uni-mannheim.de/fileadmin/lehrstuehle/pi4/content/projects/retargeting/test_sequences-videos_for_table/news_CIF.mp4",
        "3838d02cef35c855cf7c406ced8afe11d1de416e"
    )

@pytest.fixture
def ice_video():
    return _video_fixture_filename(
        "http://www.wim.uni-mannheim.de/fileadmin/lehrstuehle/pi4/content/projects/retargeting/test_sequences-videos_for_table/ice_CIF.mp4",
        "51b349ca7b339f14e100980b030090444df2bedb"
    )
