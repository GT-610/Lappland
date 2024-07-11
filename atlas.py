#! /usr/bin/env python3
# Copyright 2022-2024 GT610. Licensed under GNU GPLv3.
# Repo URL: https://codeberg.org/GT610/atlas

import argparse
import hashlib
import io
import json
import yaml
import os
import requests
import sys
import tarfile
from prettytable import PrettyTable
from tqdm import tqdm

# Local modules
from container import Container
from images import Image
import variables

check_dir()


#Load local data
def load_local(conf):
    if not os.path.isfile(atlas_conf):
        arch = check_arch()
        data = {
            'config': {
                'arch': arch,
                'version': ver
            }
        }
        with open(atlas_conf, 'w') as f:
            yaml.dump(data, f)
    with open(conf, 'r') as file:
        return yaml.load(file, Loader = yaml.SafeLoader)

#Using hashes (MD5 and SHA256) to check its status
#Calculate SHA256
def calc_sha256(data):
    return hashlib.sha256(yaml.dump(data).encode()).hexdigest()

#Calculate MD5SUMS
def calc_md5(data):
    return hashlib.md5(yaml.dump(data).encode()).hexdigest()

#Define a bool to return if the list is up to date
def is_local_list_up_to_date(remote_md5,remote_sha256):
    if not os.path.isfile(atlas_remote):
        return False
    local_data = load_local(atlas_remote)
    local_md5 = calc_md5(local_data)
    local_sha256 = calc_sha256(local_data)
    if local_md5 == remote_md5 and local_sha256 == remote_sha256:
        return True

#Show the list (called by 'images' command)
def show_list():
    if os.path.isfile(atlas_remote):
        with open(atlas_remote, 'r') as file:
            local_data = yaml.load(file,Loader=yaml.SafeLoader)
            remote_data = get_list()
            print('Checking remote list...')
            remote_sha256 = calc_sha256(remote_data)
            remote_md5 = calc_md5(remote_data)
            if is_local_list_up_to_date(remote_md5,remote_sha256):
                print("Local image list is up to date.")
                data = local_data
            else:
                print("Fetching remote image list...")
                data = remote_data
                save_local(data)
                print('Done.')
    else:
        print("Fetching remote image list.")
        data = get_list()
        save_local(data)
        print('Done.')

    config = load_local(atlas_conf)
    table = PrettyTable()
    arch = check_arch()
    table.field_names = ["Name","Version","Installed","Installable"]
    for i in data.get('linux'):
        name = i
        infos = data.get(name)
        version = infos.get ('version')
        installed = name in config.keys()
        installable = arch in infos.keys()
        table.add_row([name,version,installed,installable])
    print(table.get_string())

#Pull image
def pull_image(distro):
    arch = check_arch()
    lists = get_list()
    config = load_local()
    distro_tmp = temp_path + distro
    if distro in config.keys():
        print(distro + ' have been already installed')
        exit(1)
    if distro not in lists.keys():
        print(distro + ' isn''t avaliable')
        exit(1)
    infos = lists.get(distro)
    if arch not in infos.keys():
        print(distro + ' doesn''t support your CPU architecture')
        exit(1)
    if os.path.isfile(distro_tmp):
        print(distro + ' already downloaded, skipping downloading...')
    else:
        url = infos.get(arch)
        print('Pulling rootfs')
        r = requests.get(url,stream=True)
        if not r.status_code == 200:
            print('Something is wrong. Try again.')
            print('Network Error')
            exit(1)
        total_size = int(r.headers.get('Content-Length'))
        block_size = io.DEFAULT_BUFFER_SIZE
        t = tqdm(total=total_size,unit='iB',unit_scale=True)
        with open(temp_path + distro,'wb') as f:
            for chunk in r.iter_content(block_size):
                t.update(len(chunk))
                f.write(chunk)
        r.close()
        t.close()
    if infos.get('check') == 'ubuntu':
        check_url = 'https://partner-images.canonical.com/core/' + infos.get('version') + '/current/MD5SUMS'
        check_sum_ubuntu(distro,check_url)
    elif infos.get('check') == 'no':
        print(distro + ' has no check method')
        print('skiping')
    else:
        check_url = url + '.' + infos.get('check')
        check_sum(distro=distro,url=check_url,check=infos.get('check'))
    
    if not infos.get('zip') == 'fedora':
        extract_file(distro,infos.get('zip'))
    else:
        extract_fedora()
    config_image(distro,infos)

def remove_image(distro):
    distro_path = atlas_home + distro
    print('Removing image '+ distro)
    os.system('chmod -R 777 ' + distro_path)
    os.system('rm -rf ' + distro_path)
    config = load_local()
    del config[distro]
    with open(atlas_config,'w') as f:
        yaml.dump(config,indent=4,fp=f)


def config_image(distro,infos):
    print('Configuring image')
    distro_path = atlas_home + distro
    resolv_conf = distro_path + '/etc/resolv.conf'
    with open(resolv_conf,'w') as f:
        f.write('nameserver 1.1.1.1\n')
        f.write('nameserver 8.8.8.8\n')
    config = load_local()
    config.update({distro : infos})
    with open(atlas_config,'w') as f:
        yaml.dump(config,indent=4,fp=f)
    print('All done')
    print('Run it with atlas run ' + distro)
    
def extract_file(distro,zip_m):
    distro_path = atlas_home + distro
    file_path = temp_path + distro
    if os.path.isdir(distro_path):
        os.system('chmod -R 777 ' + distro_path)
        os.system('rm -rf ' + distro_path)

    zip_f = tarfile.open(file_path,'r:'+zip_m)
    if not os.path.isdir(distro_path):
        os.mkdir(distro_path)
    print('Extracting image')
    zip_f.extractall(distro_path,numeric_owner=True)

def extract_fedora():
    file_path = temp_path+ 'fedora'
    distro_path = atlas_home + 'fedora'
    print('Extracting image')
    zip_f = tarfile.open(file_path)
    for i in zip_f.getnames():
        if 'layer.tar' in i:
            zip_name = i
    zip_f.extract(zip_name,temp_path)
    zip_f.close()
    zip_f = tarfile.open(temp_path + zip_name,'r')
    if not os.path.isdir(distro_path):
        os.mkdir(distro_path)
    zip_f.extractall(distro_path,numeric_owner=True)
    

def check_sum(distro,url,check):
    print('Checking file integrity')
    r = requests.get(url)
    file_path = temp_path + distro
    if not r.status_code == 200:
        print('Can''t get checksum file,are you sure to continue? [y/N]',end=' ')
        a = ''
        input(a)
        if a == 'y' or a == 'Y':
            return
        else:
            print('Exiting')
            os.remove(file_path)
            exit(1)
    sum_calc = hashlib.md5() if check == 'md5' else  hashlib.sha256()
    total_size = os.path.getsize(file_path)
    block_size = io.DEFAULT_BUFFER_SIZE
    t = tqdm(total=total_size,unit='iB',unit_scale=True)
    with open(file_path,'rb') as f:
        for chunk in iter(lambda: f.read(block_size ), b''):
            t.update(len(chunk))
            sum_calc.update(chunk)
    t.close()
    f.close()

    if sum_calc.hexdigest() in r.text:
        print('Checksum successfully')
        return 0
    else:
        print('Checksum error')
        print('Removing file')
        print('Exiting')
        os.remove(file_path)
        exit(1)

def check_sum_ubuntu(distro,url):
    r = requests.get(url)
    file_path = temp_path + distro
    if not r.status_code == 200:
        print('Can''t get checksum file,are you sure to continue? [y/n]',end=' ')
        a = ''
        input(a)
        if not a == 'y':
            print('Exiting')
            os.remove(file_path)
            exit(1)
    sum_calc = hashlib.md5()
    total_size = os.path.getsize(file_path)
    block_size = io.DEFAULT_BUFFER_SIZE
    t = tqdm(total=total_size,unit='iB',unit_scale=True)
    with open(file_path,'rb') as f:
        for chunk in iter(lambda: f.read(block_size),b''):
            t.update(len(chunk))
            sum_calc.update(chunk)
    t.close()
    f.close()

    if sum_calc.hexdigest() in r.text:
        return 0
    else:
        print('Checksum error')
        print('Exiting')
        os.remove(file_path)
        exit(1)

def clean_tmps():
    print('Cleaning temporary files')
    os.system('rm -rf ' + temp_path + '*')

def run_image(arg):
    distro = arg[0]
    config = load_local()
    if not distro in config.keys():
        print('You don''t have ' + distro + 'image')
        print('Pull it before running it')
        exit(1)
    distro_path = atlas_home + distro
    infos = config.get(distro)
    command = ''
    command += 'proot'
    command += ' --link2symlink'
    command += ' -S '
    command += distro_path
#   command += ' -b /sdcard'
#   command += ' -b /system'
#   command += ' -b /data/data/com.termux/files/home'
    command += ' -w /root'
    command += ' /usr/bin/env -i'
    command += ' HOME=/root'
    command += ' LANG=C.UTF-8'
    command += ' PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin:/usr/local/sbin'
    command += ' TERM=xterm-256color'
    command += ' /bin/'
    os.unsetenv('LD_PRELOAD')
    if 'shell' in infos.keys():
        command += infos.get('shell')
    else:
        with open(distro_path+"/etc/passwd") as f:
            passwd_dict={}
            for line in f:
                args = line.split(":")
                passwd_dict[args[0]]=args[6]
            shell=passwd_dict['root'].strip().split('/')
            if (shell[-1] != '' and len(shell[-1]) != 0):
                command += shell[-1]
            else:
                command += 'bash'

    command += ' --login'
    if len(arg) > 1:
        ext_com = ' '.join(arg[1:])
        os.system(command + ' -c ' + ext_com)
    else:
        os.system(command)

# Define help message
helpmessage = 'Project atlas ' + ver + '\n\n images\t\t list remote images\n remove\t\t remove a local image\n pull\t\t pull a remote image\n run\t\t start a local image\n clean\t\t clean temporary files\n help\t\t show this detailed help'

# Parse auguments:
def parse_args():
    parser = argparse.ArgumentParser(prog='atlas',description=helpmessage)
    parser.add_argument('command', choices=['images', 'remove', 'pull', 'run', 'clean', 'help'], help='Run \'atlas help\' for detailed usage.')
    return parser.parse_args()


    

# Main func
if __name__ == "__main__":
    check_dir()
    args = parse_args()
    if args.command == 'pull':
        pull_image()
    elif args.command == 'images':
        show_list()
    elif args.command == 'remove':
        remove_image()
    elif args.command == 'run':
        run_image()
    elif args.command == 'clean':
        clean_tmps()
    elif args.command == 'help':
        print(helpmessage)
    else:
        print(helpmessage)
        exit(1)
