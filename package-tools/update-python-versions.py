import os
import sys
from pathlib import Path
from csv import DictReader


if sys.version_info.minor > 10:
    import tomllib
    import tomllib as tomllib_w
else:
    import tomli as tomllib
    import tomli_w as tomllib_w

reader = DictReader(Path("repositories.csv").open().read().split("\n"), fieldnames=["repository"])


root_path = Path("v10-release-repos").expanduser().absolute()


repo_names = [row["repository"] for row in reader ]

for repository_name in repo_names:
    print(f"Processing: {repository_name}")
    os.chdir(root_path)
    os.chdir(repository_name)

    pyproject = tomllib.load(Path("pyproject.toml").open(mode='br'))

    for package, data in pyproject['tool']['poetry']['dependencies'].items():
        if package == 'python':
            if data != '>=3.10,<4.0':
                print(f"for python package version is: {data}")
                pyproject['tool']['poetry']['dependencies'][package] = '>=3.10,<4.0'
                Path('pyproject.toml').write_text(tomllib_w.dumps(pyproject))
        # if isinstance(data, dict):
        #     print(f"f{repository_name} has invalid local resource")
        #     continue_to_next = True

# for repository_name in repo_names:
#     print(f"Processing {repository_name}")
#     os.chdir(root_path / repository_name)
#
#     pyproject = tomllib.load(Path("pyproject.toml").open(mode='br'))
#
#     continue_to_next = False
#     for package, data in pyproject['tool']['poetry']['dependencies'].items():
#         if isinstance(data, dict):
#             print(f"f{repository_name} has invalid local resource")
#             continue_to_next = True
#
#     if continue_to_next:
#         continue
