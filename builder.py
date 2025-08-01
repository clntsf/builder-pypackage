from pathlib import Path
from subprocess import run

from yamlpack.local.util import get_text, get_package_resource

def init_module(path: Path):
    """Make a module folder and __init__.py file (dummy module contents)"""
    run(["mkdir", path])
    run(["touch", f"{path}/__init__.py"])

def build_modules(path: Path, modules: list):
    """
    build modules recursively from structure specified in the YAML config
    """
    if modules is None:
        return

    for module in modules:
        if isinstance(module, str):
            init_module(Path.joinpath(path, module))

        elif isinstance(module, dict):
            module_name = list(module.keys())[0]
            module_path = Path.joinpath(path, module_name)
            init_module(module_path)
            build_modules(module_path, module[module_name])

def fill_fields(text: str, settings: dict):
    map = [
        ("@AUTHORNAME", settings["user"]["fullname"]),
        ("@AUTHOREMAIL", settings["user"]["email"]),
        ("@GITHUB", "https://github.com/" + settings["user"]["github"]),
        ("@PKGNAME", settings["package"]["name"]),
        ("@DESCRIPTION", settings["package"]["description"]),
    ]

    for (old, new) in map:
        text = text.replace(old, new)
    
    return text

def populate_package_info_files(
        package_path: Path,
        settings: dict[str, str|dict],
    ):

    def write_to_dest(destpath: str, text: str):
        with open(package_path.joinpath(destpath), "w") as writer:
            writer.write(fill_fields(text, settings))

    write_to_dest("setup.py", get_text(get_package_resource("setup.py.sample")))
    write_to_dest("LICENSE", get_text(get_package_resource("LICENSE.sample")))
    write_to_dest("pyproject.toml", get_text(get_package_resource("pyproject.toml.sample")))
    write_to_dest("README.md", "")
    write_to_dest(".gitignore", "")
    write_to_dest(f"src/{settings['package']['name']}/__main__.py", "")