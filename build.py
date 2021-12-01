#!/usr/bin/python3
import subprocess as sp
from pathlib import Path

def copy_files(dst, files):
    dst.mkdir(parents=True, exist_ok=True)
    for f in files:
        name = f.name.replace(' ', '')
        d = dst.joinpath(name)
        print('{} -> {}'.format(f, d))
        d.unlink(missing_ok=True)
        f.link_to(d)

if __name__ == '__main__':
    cwd = Path.cwd()
    build_dir = cwd.joinpath('build/debug')
    docs_dir = build_dir.joinpath('docs')
    docs_out = build_dir
    sp.check_call(['scons'])
    paper_reading = docs_dir.joinpath('_extra/paper-reading')
    copy_files(
        paper_reading.joinpath('integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization'),
        [
            cwd.joinpath('CSD-92-689.pdf'),
            build_dir.joinpath('src/integrated-placement-and-routing-for-vlsi-layout-synthesis-and-optimization/chapter1-2.notes.pdf')])
    copy_files(
        paper_reading.joinpath('almost-optimum-placement-legalization-by-minimum-cost-flow-and-dynamic-programming'),
        [cwd.joinpath('Almost Optimum Placement Legalization by Minimum Cost Flow and Dynamic Programming.pdf')])
    copy_files(
        paper_reading.joinpath('fence-region-aware-mixed-height-standard-cell-legalization'),
        [cwd.joinpath('Fence-Region-Aware Mixed-Height Standard Cell Legalization.pdf')])
    sp.check_call(['sphinx-build', '-M', 'html', f'{docs_dir}', f'{docs_out}'])
