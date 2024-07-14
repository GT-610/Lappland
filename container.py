import yaml
import datetime
import uuid
from variables import containers_path

created_containers_list_path = os.path.join(containers_path, "created_containers.yaml")

# Read containers list
def read_created_containers_list():
    # Check if created containers list path exists and create it if not
    if not os.path.exists(created_containers_list_path):
        # Create an empty file
        with open(created_containers_list_path, 'w') as f:
            pass  # This will create the file but won't write anything into it


    # Now safely open the file in read mode
    with open(created_containers_list_path, 'r') as f:
        try:
            return yaml.safe_load(f) or []
        except yaml.YAMLError as exc:
            print(f"Failed to load created containers list: {exc}")
            return []  # Return an empty list in case of any YAML parsing error

# Write containers list
def write_created_containers_list():
    with open(created_containers_list_path, 'w') as f:
        yaml.safe_dump(create_containers, f)

# Create a container
def create_container(name,image,version):  
    # Read the created containers list
    created_containers = read_created_containers_list()

    # Check if the container name exists
    for container in created_containers:
        if name == container["name"]:
            raise ValueError(f"Container '{name}' already exists.")

    # If container name isn't used, accept the creation request
   
    # Get the create time
    created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Generate a UUID to identify the container
    uuid = str(uuid.uuid4())

    # TODO: Get the version
    # version = 

    # TODO: Get the script path
    # script = 

    # Create the folder for the container
    path = os.path.join(containers_path, uuid)

    # Create a container parameter
    container = {
        uuid: {
            "name": name,
            "image": image,
            "version": version,
            "script": script,
            "created": created,
            "path": path,
        }
   }

    # Add the container into the data
    created_containers.append(container)

    # Write back to created container list
    write_created_containers_list()

# Remove a container
def remove_container(name):
    # Read created container list
    created_containers = read_created_containers_list()

    # Find the container by name and get its path
    for container in created_containers:
        if name == container["name"]:
             container_path = container["path"]
             break

    if container_path:
        # Delete the whole container's directory and its contents
        shutil.rmtree(container_path)

        # Remove the container from data
        data = [c for c in created_containers_list_path if c["name"] != name]

        # Write containers.list
        write_created_containers_list()
    
    else:
        raise ValueError(f"Container '{name}' not found.")

# Rename a container
def rename_container():
    # Read the created container list
    created_containers = read_created_containers_list()

    # Find the container by old_name and get its index
    for container in created_containers:
        if old_name == container["name"]:
            # TODO: Get the container UUID
            # container_uuid = 
            break

        if container_index is not None:
            # Modify the name of the container
            create_containers[uuid]["name"] = new_name

            # Write back to list.yaml
            write_created_containers_list()

        # The program doesn't support removing air
        else:
            raise ValueError(f"Container '{old_name}' not found.")

def start_container(name):
    pass
