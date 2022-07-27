import os
import shutil
import pytest
import skillsnetwork

from pathlib import Path
from pytest_httpserver import httpserver
from random import choice
from string import ascii_uppercase


def test_backwards_compatibility():
    assert skillsnetwork.read == skillsnetwork.read_dataset
    assert skillsnetwork.download == skillsnetwork.download_dataset


@pytest.mark.asyncio
async def test_read(httpserver):
    url = "/test"
    expected_data = "".join(choice(ascii_uppercase) for i in range(10000))
    httpserver.expect_request(url).respond_with_data(expected_data)

    data = await skillsnetwork.read(httpserver.url_for(url))
    assert data.decode("utf-8") == expected_data


@pytest.mark.asyncio
async def test_download(httpserver):
    url = "/test"
    filename = "test.txt"
    expected_data = "".join(choice(ascii_uppercase) for _ in range(10000))
    httpserver.expect_request(url).respond_with_data(expected_data)

    await skillsnetwork.download(httpserver.url_for(url), path=filename)
    with open(filename, "r") as f:
        assert expected_data == f.read()
        os.remove(filename)


@pytest.mark.asyncio
async def test_prepare_dataset_url_does_not_exist():
    with pytest.raises(Exception):
        await skillsnetwork.prepare_dataset(
            "https://example.com/does-not-exist.tar.gz",
            path="test",
        )


@pytest.mark.asyncio
async def test_prepare_dataset_invalid_url():
    with pytest.raises(skillsnetwork.InvalidURLException):
        await skillsnetwork.prepare_dataset("bad_url")


@pytest.mark.asyncio
async def test_prepare_dataset_tar_no_path(httpserver):
    url = "/test.tar.gz"
    expected_directory = "test"
    try:
        shutil.rmtree(expected_directory)  # clean up any previous test
    except FileNotFoundError as e:
        print(e)
        pass

    with open("tests/test.tar.gz", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url))

    assert os.path.isdir(expected_directory)
    with open(expected_directory + "/1.txt") as f:
        assert "I am the first test file" in f.read()
    os.unlink(expected_directory)


@pytest.mark.asyncio
async def test_prepare_dataset_tar_with_path(httpserver):
    url = "/test.tar.gz"
    path = "example"
    try:
        shutil.rmtree(path)  # clean up any previous test
    except FileNotFoundError:
        pass

    with open("tests/test.tar.gz", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url), path=path)
    assert os.path.isdir(path)
    shutil.rmtree(path)


@pytest.mark.asyncio
async def test_prepare_dataset_zip_no_path(httpserver):
    url = "/test.zip"
    expected_directory = "test"
    try:
        shutil.rmtree(expected_directory)  # clean up any previous test
    except FileNotFoundError as e:
        print(e)
        pass

    with open("tests/test.zip", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url))

    assert os.path.isdir(expected_directory)
    with open(expected_directory + "/1.txt") as f:
        assert "I am the first test file" in f.read()
    os.unlink(expected_directory)


@pytest.mark.asyncio
async def test_prepare_dataset_zip_with_path(httpserver):
    url = "/test.zip"
    path = "tests/example"
    try:
        shutil.rmtree(path)  # clean up any previous test
    except FileNotFoundError:
        pass

    with open("tests/test.zip", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url), path=path)
    assert os.path.isdir(path)
    shutil.rmtree(path)


@pytest.mark.asyncio
async def test_prepare_non_compressed_dataset_with_path(httpserver):
    url = "/test.csv"
    path = "."
    expected_path = Path("./test.csv")
    with open("tests/test.csv", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url), path=path)
    assert expected_path.exists()
    expected_path.unlink()


@pytest.mark.asyncio
async def test_prepare_non_compressed_dataset_no_path_with_overwrite(httpserver):
    url = "/test.csv"
    expected_path = Path("./test.csv")
    with open("tests/test.csv", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url))
    assert expected_path.exists()
    httpserver.clear()
    with open("tests/test.csv", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url), overwrite=True)
    assert expected_path.exists()
    assert Path(expected_path).stat().st_size == 540
    expected_path.unlink()


@pytest.mark.asyncio
async def test_prepare_dataset_tar_no_path_with_overwrite(httpserver):
    url = "/test.tar.gz"
    expected_directory = Path("test")
    try:
        shutil.rmtree(expected_directory)  # clean up any previous test
    except FileNotFoundError as e:
        print(e)
        pass

    with open("tests/test.tar.gz", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url))

    assert os.path.isdir(expected_directory)
    with open(expected_directory / "1.txt") as f:
        assert "I am the first test file" in f.read()
    httpserver.clear()

    with open("tests/test.tar.gz", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url), overwrite=True)
    assert os.path.isdir(expected_directory)
    with open(expected_directory / "1.txt") as f:
        assert "I am the first test file" in f.read()
    expected_directory.unlink()


@pytest.mark.asyncio
async def test_prepare_dataset_zip_no_path_with_overwrite(httpserver):
    url = "/test.zip"
    expected_directory = Path("test")
    try:
        shutil.rmtree(expected_directory)  # clean up any previous test
    except FileNotFoundError as e:
        print(e)
        pass

    with open("tests/test.zip", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url))

    assert os.path.isdir(expected_directory)
    with open(expected_directory / "1.txt") as f:
        assert "I am the first test file" in f.read()
    httpserver.clear()

    with open("tests/test.zip", "rb") as expected_data:
        httpserver.expect_request(url).respond_with_data(expected_data)
        await skillsnetwork.prepare_dataset(httpserver.url_for(url), overwrite=True)
    assert os.path.isdir(expected_directory)
    with open(expected_directory / "1.txt") as f:
        assert "I am the first test file" in f.read()
    expected_directory.unlink()
