"""Copy the editable KMFA starter to a new or empty directory. Stdlib only."""
import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / 'assets' / 'kmfa-starter'
    destination = args.destination.expanduser().resolve()
    skill = source.parents[1]
    if destination == skill or skill in destination.parents:
        parser.error('Choose an output directory outside the skill directory.')
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        parser.error('Destination must be new or empty; nothing was overwritten.')
    files = sorted(p for p in source.rglob('*') if p.is_file())
    if not files:
        parser.error('Starter assets are missing.')
    destination.mkdir(parents=True, exist_ok=True)
    for p in files:
        target = destination / p.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
    print(f'Created {len(files)} files in {destination}')
    print('Next: adapt the model and references, run Blender, npm ci, npm run build.')


if __name__ == '__main__':
    main()
