import os
import requests
import yaml

# Load modules
from variables import atlas_home, registries_path, check_dir
# from userinput import prefix_image

registries_yaml_path = os.path.join(registries_path, 'registries.yaml')

# Get the registries list
def check_registeries_list():
    if not os.path.exists(registries_yaml_path):
        print("Registries list not found. fetching from repository...")
        response = requests.get("https://cdn.jsdelivr.net/gh/GT-610/atLAs@master/src/registries.yaml")
        if response.status_code == 200:
            with open(registries_yaml_path, 'w') as file:
                file.write(response.text)
            print(f"Registries list fetched successfully. Saved at {registries_path}.")
        else:
            print(f"Failed to fetch registries list. Status code: {response.status_code}")


# Read the registeries list
# Returns: Specified prefix && location
def read_registries_list(registries_yaml_path, prefix_image):
    with open(registries_yaml_path, 'r') as stream:
        try:
            registries = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(f"Error in reading registries list: {e}")
       
    # Parse the prefix
    prefix, _ = prefix_image.split('/')

    for reg_name, reg_details in registries['registries'].items():
        print(reg_name)
        if reg_details.get('prefix') == prefix:
            return reg_name, reg_details['prefix'], reg_details['location']

    print(f"Registry {prefix} not defined in registries list.")
    return None, None, None

# Fetch the remote registry
# Returns: parsed remote YAML text
def fetch_remote_registry(prefix, location):
    print(f"Fetching {prefix}...")
    response = requests.get(location)
    if response.status_code == 200:
        remote_yaml = yaml.safe_load(response.text)
        return remote_yaml
    else:
        print(f"Failed to reach list of {prefix}. Status code: {response.status_code}")
        return None


# Parse the remote registry
# Returns: Image information
def read_image(remote_yaml, prefix_image, arch):
    # Parse the image name
    _, image_name = prefix_image.split('/')

    if image_name in remote_yaml.get('images', {}):
        print(remote_yaml)
        image = remote_yaml['images'][image_name]

        # 查找匹配架构的版本信息
        for version in image.get('variants', []):
            if version['arch'] == arch:
                url = image.get('base_url') + version.get('file')
                # 返回找到的详细信息
                return {
                    'prefix': image_name,
                    'url': url,
                    'arch': version.get('arch'),
                    'sha256': version.get('sha256'),
                }
    print("Failed to read image information in the registry list.")
    return None