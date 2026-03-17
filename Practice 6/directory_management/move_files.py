from pathlib import Path

# List only Python files
for p in Path('.').rglob('*.py'):
    print(p.name)