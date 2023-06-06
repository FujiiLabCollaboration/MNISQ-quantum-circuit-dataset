import sys
import os
import subprocess
import zipfile

# def zip_subdirs(root_dir):
#     for subdir in os.listdir(root_dir):
#         subdir_path = os.path.join(root_dir, subdir)
#         if os.path.isdir(subdir_path):
#             with zipfile.ZipFile(subdir + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
#                 for file in os.listdir(subdir_path):
#                     file_path = os.path.join(subdir_path, file)
#                     zip_file.write(file_path, file)

def zip_subdirs(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for subdir in dirs:
            cp = subprocess.run(['zip', '-r', f'{subdir}.zip', subdir])
            if cp.returncode != 0:
                print('zip failed.', file=sys.stderr)
                sys.exit(1)

            # # サブディレクトリのパス
            # subdir_path = os.path.join(root, subdir)
            # # zipファイル名
            # zip_name = subdir_path + '.zip'
            # # zipファイルを作成し、サブディレクトリ内のファイルを圧縮する
            # with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            #     for file in os.listdir(subdir_path):
            #         file_path = os.path.join(subdir_path, file)
            #         if os.path.isfile(file_path):
            #             zipf.write(file_path, file)


if __name__ == '__main__':
    dirpath = sys.argv[1]
    zip_subdirs(dirpath)
