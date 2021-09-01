#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os

if __name__ == '__main__':
    cwd = Path.cwd()
    uid = os.getuid()
    gid = os.getgid()
    cmd = ['docker', 'run', '--rm', 
        # '--user', '%d:%d' % (uid, gid),
        '-v', '%s:/opt/code' % cwd, 
        'taoda-base', 
        'make', 'html']
    print(' '.join(cmd))
    sp.run(cmd).check_returncode()
    print()
    print('The entry point is:', Path('build/html/index.html').absolute())
    