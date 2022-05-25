import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--directory", "-d", default=None, required=True, type=str, help="target directory")
args = parser.parse_args()

target_directory = args.directory

def copy_recursively(path, base_path="."):
    path = f"{base_path}/{path}"
    os.system(f"cp index.php {path}")
    sub_paths = [x for x in os.listdir(path) if os.path.isdir(f"{path}/{x}")]
    
    if len(sub_paths) == 0:
        return
    else:
        for p in sub_paths:
            copy_recursively(p, path)

if __name__ == "__main__":
    copy_recursively(target_directory)
