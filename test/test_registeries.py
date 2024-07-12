# registries.py test suite
# Run "pytest --capture=sys test_registeries.py" to test this
import os
import pytest
from unittest.mock import patch
import requests
import sys

# Load the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from registries import *
from variables import atlas_home, registries_path
registries_yaml_path = os.path.join(registries_path, 'registries.yaml')

# Check if directories exist
check_dir()

@patch('requests.get')
def test_check_registeries_list_when_file_does_not_exist(mock_get, capsys):
    if os.path.exists(registries_yaml_path):
        os.remove(registries_yaml_path)

    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "Mocked registries data"
    
    check_registeries_list()

    # Check the output
    captured = capsys.readouterr()
    assert "Registries list not found. fetching from repository..." in captured.out
    assert "Registries list fetched successfully." in captured.out

    # Check if mocked reg data is written
    assert os.path.exists(registries_path)
    with open(registries_yaml_path, 'r') as f:
        assert f.read() == "Mocked registries data"

@patch('requests.get')
def test_check_registeries_list_but_response_fail(mock_get, capsys):
    if os.path.exists(registries_yaml_path):
        os.remove(registries_yaml_path)

    mock_get.return_value.status_code = 404
    
    check_registeries_list()

    # Check the output
    captured = capsys.readouterr()
    assert "Registries list not found. fetching from repository..." in captured.out
    assert "Failed to fetch registries list. Status code: 404" in captured.out

@patch('requests.get')
def test_read_registries_list_while_prefix_exists(mock_get, capsys):
    if os.path.exists(registries_yaml_path):
        os.remove(registries_yaml_path)

    mock_get.return_value.status_code = 200
    mock_get.return_value.text = """
    registries:
        example_reg:
            prefix: "example"
            location: "https://example.com/example_image_list.yaml"
    """

    check_registeries_list()
    reg_name, prefix, location = read_registries_list(registries_yaml_path, "example/eximage")

    captured = capsys.readouterr()
    print(captured.out)
    assert "Registries list not found. fetching from repository..." in captured.out
    assert "Registries list fetched successfully." in captured.out

    assert reg_name == "example_reg"
    assert prefix == "example"
    assert location == "https://example.com/example_image_list.yaml"

@patch('requests.get')
def test_read_registries_list_while_prefix_does_not_exist(mock_get, capsys):
    if os.path.exists(registries_yaml_path):
        os.remove(registries_yaml_path)

    mock_get.return_value.status_code = 200
    mock_get.return_value.text = """
    registries:
        example_reg:
            prefix: "example"
            location: "https://example.com/example_image_list.yaml"
    """

    check_registeries_list()
    reg_name, prefix, location = read_registries_list(registries_yaml_path, "foo/bar")

    captured = capsys.readouterr()
    print(captured.out)
    assert "Registries list not found. fetching from repository..." in captured.out
    assert "Registries list fetched successfully." in captured.out

    assert reg_name == None
    assert prefix == None
    assert location == None
    assert "Registry foo not defined in registries list." in captured.out

@patch('requests.get')
def test_fetch_remote_registry_while_success(mock_get, capsys):
    if os.path.exists(registries_yaml_path):
        os.remove(registries_yaml_path)

    mock_get.return_value.status_code = 200
    mock_get.return_value.text = """
    images:
        eximage:
          name: "Example image"
          base_url: "https://example.com/images"
          variants:
            - arch: aarch64
              file: "eximage-aarch64.tar.xz"
              sha256: "000001"

            - arch: x86_64
              file: "eximage-x86_64.tar.xz"
              sha256: "000002"
          version: 24.07

        not_an_eximage:
          name: "Not an example image"
          base_url: "https://example.com/images"
          variants:
            - arch: aarch64
              file: "notaneximage-aarch64.tar.xz"
              sha256: "000003"

            - arch: x86_64
              file: "notaneximage-x86_64.tar.xz"
              sha256: "000005"
          version: 8.9
    update: '2024-07-10'
    """

    remote_reg_data = fetch_remote_registry("example", "https://example.com/example_image_list.yaml")
    
    captured = capsys.readouterr()
    assert "Fetching example..." in captured.out
    assert remote_reg_data == {
        'images': {
            'eximage': {
                'name': 'Example image',
                'base_url': 'https://example.com/images',
                'variants':[{
                    'arch': 'aarch64',
                    'file': 'eximage-aarch64.tar.xz',
                    'sha256': '000001'
                }, {
                    'arch': 'x86_64',
                    'file': 'eximage-x86_64.tar.xz',
                    'sha256': '000002'
                }],
                'version': 24.07
            }, 
            'not_an_eximage': {
                'name': 'Not an example image',
                'base_url': 'https://example.com/images',
                'variants': [{
                    'arch': 'aarch64',
                    'file': 'notaneximage-aarch64.tar.xz',
                    'sha256': '000003'
                }, {
                    'arch': 'x86_64',
                    'file': 'notaneximage-x86_64.tar.xz',
                    'sha256': '000005'}],
                    'version': 8.9
            },
        },
        'update': '2024-07-10'
    }

@patch('requests.get')
def test_fetch_remote_registry_but_404(mock_get, capsys):
    if os.path.exists(registries_yaml_path):
        os.remove(registries_yaml_path)

    mock_get.return_value.status_code = 404

    remote_reg_data = fetch_remote_registry("example", "https://example.com/example_image_list.yaml")
    
    captured = capsys.readouterr()
    assert "Failed to reach list of example. Status code: 404" in captured.out
    assert remote_reg_data == None

def test_read_image_success(capsys):
    remote_yaml_text = """
    images:
        eximage:
          name: "Example image"
          base_url: "https://example.com/images"
          variants:
            - arch: aarch64
              file: "eximage-aarch64.tar.xz"
              sha256: "000001"

            - arch: x86_64
              file: "eximage-x86_64.tar.xz"
              sha256: "000002"
          version: 24.07

        not_an_eximage:
          name: "Not an example image"
          base_url: "https://example.com/images"
          variants:
            - arch: aarch64
              file: "notaneximage-aarch64.tar.xz"
              sha256: "000003"

            - arch: x86_64
              file: "notaneximage-x86_64.tar.xz"
              sha256: "000005"
          version: 8.9
    update: '2024-07-10'
    """
    remote_yaml = yaml.safe_load(remote_yaml_text)
    image_data = read_image(remote_yaml, "example/eximage", "aarch64")

    assert image_data["prefix"] == "eximage"