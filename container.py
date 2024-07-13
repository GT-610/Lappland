import yaml
import datetime
import uuid
from variables import containers_path

def create_container(self,name,image,version):
        
   # TODO: Read the created containers list
   

   # Check if the container name exists
   for container in created_containers:
       if name == container["name"]:
           raise ValueError(f"Container '{name}' already exists.")

   # If container name isn't used, accept the creation request

   # Generate a UUID to identify the container
   uuid = str(uuid.uuid4())

   # Get the create time
   created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

   # Create the folder for the container
   path = containers_path + uuid

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
   created_containers.append(container)

   # Write back to created container list


# Remove a container
def remove_container(self, name):
    # TODO: Read created container list

    # Find the container by name and get its path
    for container in created_containers:
        if name == container["name"]:
             container_path = os.path.join(containers_path, container.get("path"))
             break

    if container_path:
         # Delete the whole container's directory and its contents
         shutil.rmtree(container_path)

         # Remove the container from data
         data = [c for c in data if c["name"] != name]

         # TODO: Write back to list.yaml
    
    else:
         raise ValueError(f"Container '{name}' not found.")

# Rename a container
def rename_container():
    # TODO: Read the created container list

    container_index = None

    # Find the container by old_name and get its index
    for index, container in enumerate(created_containers):
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
