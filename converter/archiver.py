import sys
import os
import subprocess

def zip_subdirs(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for subdir in dirs:
            cp = subprocess.run(['zip', '-r', f'{subdir}.zip', subdir])
            if cp.returncode != 0:
                print('zip failed.', file=sys.stderr)
                sys.exit(1)

if __name__ == '__main__':
    dirpath = sys.argv[1]
    zip_subdirs(dirpath)
