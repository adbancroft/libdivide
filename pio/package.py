import os
from pathlib import Path
from packaging.version import parse as parse_version
import json

def get_version(libdivide_h):
    with libdivide_h.open() as f:
        versions = [l for l in f.readlines() if "LIBDIVIDE_VERSION_" in l]
        major_ver = [v for v in versions if "LIBDIVIDE_VERSION_MAJOR" in v][0].split()[2]
        minor_ver = [v for v in versions if "LIBDIVIDE_VERSION_MINOR" in v][0].split()[2]

        return parse_version(major_ver + "." + minor_ver)

def package(sourcedir, targetdir):
    libdivide_h = sourcedir / "libdivide.h"
    library_json = targetdir / "library.json"
    with library_json.open() as f:
        library_json_raw = json.load(f)

    library_json_raw["version"] = str(get_version(libdivide_h))

    with library_json.open(mode='w') as f:
        json.dump(library_json_raw, f, indent=4)
    
if __name__ == "__main__":
    targetdir = Path(os.path.dirname(os.path.abspath(__file__)))
    package(targetdir.parent, targetdir) 
    