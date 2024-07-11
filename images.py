from variables import image_path
from registries import read_registries_list

# Load modules
from registries import read_image
from variables import atlas_home, registries_path
from userinput import prefix_image

registries_yaml_path = os.path.join(registries_path, 'registries.yaml')
image_info = read_image(registries_yaml_path, prefix_image)

def pull_image(image_info):
    
