import os
import subprocess
import sys
from pathlib import Path
from csv import DictReader
import shutil
from subprocess import CalledProcessError

if sys.version_info.minor > 10:
    import tomllib
else:
    import tomli as tomllib

from git import Repo
import yaml

repository_list = yaml.safe_load(Path("repositories.yml").open())

# reader = DictReader(Path("repositories.csv").open().read().split("\n"), fieldnames=["repository"])

use_upstream = True
as_dry_run = False

root_path = Path("v10-release-repos").expanduser().absolute()

shutil.rmtree(root_path, ignore_errors=True)
root_path.mkdir(parents=True, exist_ok=True)

clone = "git@github.com:eclipse-volttron/{repository_name}.git"

#repo_names = [row["repository"] for row in reader if not row["repository"].startswith("#") ]

for repository_name in repository_list:
    os.chdir(root_path)
    print(f"Cloning {repository_name}")
    repo = Repo.clone_from(clone.format(repository_name=repository_name),
                           to_path=repository_name)

    repo.git.checkout("v10")

for repository_name in repository_list:
    print(f"Processing {repository_name}")
    os.chdir(root_path / repository_name)
    os.mkdir("./tmpenv")
    env_copy = os.environ.copy()

    # Hack for using own environment
    env_copy['POETRY_VIRTUALENVS_IN_PROJECT'] = "false"
    env_copy['POETRY_VIRTUALENVS_PATH'] = "./tempenv"
    pyproject = tomllib.load(Path("pyproject.toml").open(mode='br'))

    continue_to_next = False

    for package, data in pyproject['tool']['poetry']['dependencies'].items():
        if isinstance(data, dict):
            print(f"f{repository_name} has invalid local resource")
            continue_to_next = True

    has_dev = False
    if 'group' in pyproject['tool']['poetry']:
        has_dev = 'dev' in pyproject['tool']['poetry']['group']

    if continue_to_next:
        continue

    if has_dev:
        subprocess.check_call(args="poetry install --without dev".split(), env=env_copy)
    else:
        subprocess.check_call(args="poetry install".split(), env=env_copy)
    subprocess.check_call(args="poetry build".split(), env=env_copy)

    if as_dry_run:
        subprocess.check_call(args="poetry publish --dry-run".split(), env=env_copy)
    else:
        try:
            output = subprocess.check_output(args="poetry publish".split(), env=env_copy)
        except CalledProcessError as e:
            print(f"E is: {e}")
            print(f"stderr is: {e.stderr}")
            print(f"stdout is: {e.stdout}")
            print(f"output is: {e.output}")
            if e.stderr:
                if 'File already exists' in e.stderr:
                    print(f"{repository_name} needs to be updated to push to pypi")
                else:
                    print(e.stderr)


    #cmd_build = "poetry install --without dev"
    #subprocess.check_call([cmd_build])

    # print(f"Cloning {repository_name}")
    # repo = Repo.clone_from(clone.format(repository_name=repository_name),
    #                        to_path=repository_name)
    #
    # repo.git.checkout("v10")

