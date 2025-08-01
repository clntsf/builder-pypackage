from pathlib import Path
from subprocess import run

from .builder import populate_package_info_files, init_module, build_modules

def build(package_fp: Path, settings: dict):

    package_abspath = package_fp.resolve()
    populate_package_info_files(package_abspath, settings)

    package_cfg = settings["package"]
    name = package_cfg["name"]

    srcpath = package_abspath.joinpath(f"src/{name}")
    run(["mkdir", f"{package_abspath}/src"])
    init_module(srcpath)

    modules: list[str|dict] = package_cfg["modules"]
    build_modules(srcpath, modules)

    boilerplate = ["README.md", ".gitignore", f"src/{name}/__main__.py"]
    for filepath in boilerplate:
        run(["touch", f"{package_abspath}/{filepath}"])