import json
import os
import shutil
import subprocess

import pytest
from skillsnetwork import cvstudio


# @pytest.fixture(scope="session", autouse=True)
# def set_cvstudio_config():
#     # secret_env = subprocess.check_output(["sops", "-d", "./tests/cvstudio_config.json"])
#     with open("./tests/cvstudio_config.json") as f:
#         cv_studio_config = json.load(f)
#     for key, value in cv_studio_config.items():
#         os.environ[key] = value


def test_ping():
    training_run_token = os.environ["TRAINING_RUN_TOKEN"]
    base_url = os.environ["CV_STUDIO_BASE_URL"]
    cvstudio_client = cvstudio.CVStudio(token=training_run_token)

    assert cvstudio_client.ping().ok


def test_get_annotations():
    training_run_token = os.environ["TRAINING_RUN_TOKEN"]
    base_url = os.environ["CV_STUDIO_BASE_URL"]
    cvstudio_client = cvstudio.CVStudio(token=training_run_token)

    annotations = cvstudio_client.get_annotations()
    assert "version" in annotations
    assert "type" in annotations
    assert "labels" in annotations
    assert "annotations" in annotations


def test_download_all():
    training_run_token = os.environ["TRAINING_RUN_TOKEN"]
    base_url = os.environ["CV_STUDIO_BASE_URL"]
    cvstudio_client = cvstudio.CVStudio(token=training_run_token)

    images_dir = "images"
    if os.path.isdir(images_dir):
        shutil.rmtree(images_dir)

    cvstudio_client.downloadAll()
    assert os.path.isdir(images_dir)
    assert len(os.listdir(images_dir)) > 0
    shutil.rmtree(images_dir)
