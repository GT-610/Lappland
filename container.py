import yaml
import datetime
import uuid
from images import Image

# Necessary variables
home = os.getenv('HOME')
lappland_home = home + '/.config/lappland/'
temp_path  = lappland_home + 'tmp/'
container_path=lappland_home + "containers/"

# Container main class
class Container:

    def __init__(self,name,image,version):
        self.name=name
        self.image=image
        self.version=version

    def create_container(self,name,image,version):
        # Try to open list.yaml in append mode, this will create the file if it doesn't exist
        # If it exists, this will just pass 
        with open('list.yaml', 'a'):
            pass
        
        # Read list.yaml
        with open('list.yaml', 'r') as f:
            data = yaml.safe_load(f)

        # Check if the container name exists
        for container in data:
            if name == container["name"]:
                raise ValueError(f"Container '{name}' already exists.")

        # When everything is ready, start creating the container

        # Generate a UUID to identify the container
        uuid = str(uuid.uuid4())

        # Get the create time
        created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create the folder for the container
        path = container_path + uuid

        # Create a container parameter
        container = {
            "name": name,
            "uuid": uuid,
            "image": image,
            "version": version,
            "created": created,
            "path": path,
        }

        # Add the container into the data
        data.append(container)

        # Write back to list.yaml
        with open('list.yaml', 'w') as f:
            yaml.safe_dump(data, f)

    # Delete a container
    def delete_container(self, name):
        # Read list.yaml
        with open('list.yaml', 'r') as f:
            data = yaml.safe_load(f)

        container_path = None

        # Find the container by name and get its path
        for container in data:
            if name == container["name"]:
                container_path = container.get("path")
                break

        if container_path:
            # Delete the container's directory and its contents
            shutil.rmtree(container_path)

            # Remove the container from data
            data = [c for c in data if c["name"] != name]

            # Write back to list.yaml
            with open('list.yaml', 'w') as f:
                yaml.safe_dump(data, f)
        else:
            raise ValueError(f"Container '{name}' not found.")

    # Change the name of a container
    def change_name(self,new_name,previous_name):
        # Read list.yaml
        with open('list.yaml', 'r') as f:
            data = yaml.safe_load(f)

        container_index = None

        # Find the container by old_name and get its index
        for index, container in enumerate(data):
            if old_name == container["name"]:
                container_index = index
                break

        if container_index is not None:
            # Modify the name of the container
            data[container_index]["name"] = new_name

            # Write back to list.yaml
            with open('list.yaml', 'w') as f:
                yaml.safe_dump(data, f)

        # The program doesn't support removing air
        else:
            raise ValueError(f"Container '{old_name}' not found.")

    # def start_container(uuid):
    # def start_container_by_name(name):
    # def stop_container(uuid):