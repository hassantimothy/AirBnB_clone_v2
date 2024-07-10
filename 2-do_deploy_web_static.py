#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""

from fabric.api import env, put, run
import os.path

env.hosts = ['<IP web-01>', '<IP web-02>']

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.isfile(archive_path):
        return False
    
    try:
        # Upload the archive
        file_name = os.path.basename(archive_path)
        folder_name = file_name.split('.')[0]
        put(archive_path, "/tmp/{}".format(file_name))
        
        # Create target directory
        run('mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        
        # Uncompress archive
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(file_name, folder_name))
        
        # Remove archive
        run('rm /tmp/{}'.format(file_name))
        
        # Move files
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(folder_name, folder_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(folder_name))
        
        # Remove old symbolic link
        run('rm -rf /data/web_static/current')
        
        # Create new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))
        
        print("New version deployed!")
        return True
    except:
        return False