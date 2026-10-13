"""Check publication scope and local documentation links without network or execution."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
files = []
for path in ROOT.rglob('*'):
    relative = path.relative_to(ROOT)
    if set(relative.parts) & {'.git', '__pycache__'}:
        continue
    if path.is_symlink():
        errors.append(f'{relative}: symlinks are outside publication scope')
        continue
    if not path.is_file():
        continue
    files.append(path)
    if path.suffix not in {'.md', '.py'} and path.name not in {'Makefile', '.gitignore'}:
        errors.append(f'{relative}: unexpected public file type')
    try:
        body = path.read_text()
    except UnicodeError:
        errors.append(f'{relative}: non-text content')
        continue
    if path.suffix != '.md':
        continue
    for pattern in (r'/Users/[^\s]+', r'-----BEGIN .*PRIVATE KEY-----',
                    r'\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}',
                    r'Bearer\s+[A-Za-z0-9._-]{20,}',
                    r'\b(?:\d{1,3}\.){3}\d{1,3}\b'):
        if re.search(pattern, body):
            errors.append(f'{relative}: potential private data; review required')
    for target in re.findall(r'\]\(([^)]+)\)', body):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
            continue
        candidate = (path.parent / target.split('#')[0]).resolve()
        if not candidate.is_relative_to(ROOT) or not candidate.is_file():
            errors.append(f'{relative}: missing or out-of-scope link {target}')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'PASS: {len(files)} text files; local documentation links and publication checks')
