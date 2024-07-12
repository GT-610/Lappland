from variables import image_path
from registries import read_registries_list
import hashlib

# Load modules
from registries import read_image
from variables import image_path, registries_path, arch
from userinput import prefix_image

registries_yaml_path = os.path.join(registries_path, 'registries.yaml')
image_info = read_image(registries_yaml_path, prefix_image)



# Pull image
def pull_image(prefix_image, image_data):
    url = image_data["url"]
    print(f'Pulling {prefix_image}...')
    
    # Fetch image
    r = requests.get(url,stream=True)
    if not r.status_code == 200:
        print(f'Pulling {prefix_image} failed. Status code: {r.status_code}')
        return None
    
    image_storage_path = os.path.join(image_path, prefix_image)

    # Create a folder to store the image
    if not os.path.exists(image_storage_path):
        os.makedirs(image_storage_path)

    # Write the image into specified file path
    total_size = int(r.headers.get('Content-Length'))
    block_size = io.DEFAULT_BUFFER_SIZE
    t = tqdm(total=total_size,unit='iB',unit_scale=True)
    with open(os.path.join(image_storage_path, image_data["filename"]), 'wb') as f:
        for chunk in r.iter_content(block_size):
            t.update(len(chunk))
            f.write(chunk)
    t.close()

    r.close()

    # Check SHA256 for integrity
    print(f'Verifying integrity of {prefix_image} using SHA256...')
    sha256_hash = hashlib.sha256()
    
    # Calculate SHA256
    with open(os.path.join(image_path, image_data["filename"]), 'rb') as f:
        while True:
            data = f.read(io.DEFAULT_BUFFER_SIZE)
            if not data:
                break
            sha256_hash.update(data)

    # Compare
    if sha256_hash.hexdigest() != image_data['sha256']:
        print(f'SHA256 verification failed for {prefix_image}. Expected {image_data["sha256"]}, got {sha256_hash.hexdigest()}')
        return None
    else:
        print(f'SHA256 verification passed for {prefix_image}.')

def remove_image(prefix_image):
    image_storage_path = os.path.join(image_path, prefix_image)

    if os.path.exists(image_storage_path):
        print(f'Removing {prefix_image}...')
        try:
            shutil.rmtree(image_storage_path)
            print(f'{prefix_image} has been successfully removed.')

        except OSError as e:
            print(f'Removing {prefix_image} failed: {e.strerror}')

    else:
        print(f'{prefix_image} does not exist. Nothing to do.')
        return None


