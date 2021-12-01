#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import shutil as sh

if __name__ == '__main__':
    cwd = Path.cwd()
    build_dir = cwd.joinpath('build/debug')
    docs_dir = build_dir.joinpath('docs')
    docs_out = build_dir
    sp.check_call(['scons'])
    docs_extra = docs_dir.joinpath('_extra/paper-reading/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization')
    docs_extra.mkdir(parents=True, exist_ok=True)
    sh.copy(cwd.joinpath('CSD-92-689.pdf'), docs_extra)
    sh.copy(
        build_dir.joinpath('slides/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/chapter1-2.notes.pdf'),
        docs_extra.joinpath('chapter1-2.slides.pdf'),
    )
    sp.check_call(['sphinx-build', '-M', 'html', f'{docs_dir}', f'{docs_out}'])
