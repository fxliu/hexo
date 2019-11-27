# -*- coding: gbk -*-
"""
编译，并复制到发布目录
"""
import os
import shutil
import glob

src_path = os.path.join(os.path.dirname(__file__), 'public')
publish_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..\\..\\fxliu.github.io'))


def clean():
    print('clean: ' + src_path)
    if os.path.exists(src_path):
        shutil.rmtree(src_path)
    print('clean: ' + publish_path)
    files = glob.glob(publish_path + '\\*')
    for f in files:
        fn = os.path.basename(f)
        if fn in ['LICENSE', 'README.md', '0']:
            continue
        if os.path.isfile(f):
            os.remove(f)
        else:
            shutil.rmtree(f)


def start():
    clean()
    os.system('hexo g')
    print('publish')
    files = glob.glob(src_path + '\\*')
    for f in files:
        if os.path.isdir(f):
            shutil.copytree(f, os.path.join(publish_path, os.path.basename(f)))
        else:
            shutil.copy(f, os.path.join(publish_path, os.path.basename(f)))


if __name__ == "__main__":
    start()
