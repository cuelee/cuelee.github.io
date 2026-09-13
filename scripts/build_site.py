"""Assemble only approved public files. No upload or deployment occurs."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'publish'
FILES = (
    'index.html', 'publications.html', 'contact.html',
    'style.css', 'favicon.svg', 'profile.jpg', 'CV.pdf',
)


def main():
    subprocess.run([sys.executable, str(ROOT / 'scripts/check_site.py')], check=True)
    for name in FILES:
        source = ROOT / name
        if source.is_symlink() or not source.is_file():
            raise SystemExit(f'Expected a regular source file: {source}')
    if OUTPUT.is_symlink():
        raise SystemExit('Refusing to build into a symlink: publish/')
    if OUTPUT.exists():
        unexpected = {p.name for p in OUTPUT.iterdir()} - set(FILES)
        if unexpected:
            raise SystemExit(f'Remove unexpected files from publish/ before building: {sorted(unexpected)}')
        for target in OUTPUT.iterdir():
            if target.is_symlink() or not target.is_file():
                raise SystemExit(f'Expected a regular generated file: {target}')
    OUTPUT.mkdir(exist_ok=True)
    for name in FILES:
        shutil.copyfile(ROOT / name, OUTPUT / name)
    subprocess.run([sys.executable, str(ROOT / 'scripts/check_site.py'), str(OUTPUT)], check=True)
    print(f'Ready: {OUTPUT} ({len(FILES)} files). Upload its contents, not the project folder.')


if __name__ == '__main__':
    main()
