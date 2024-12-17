from datasets import load_dataset
from typing import Dict
from swebench_docker.constants import MAP_VERSION_TO_INSTALL_DJANGO, MAP_VERSION_TO_INSTALL_REQUESTS, MAP_VERSION_TO_INSTALL_SKLEARN, MAP_VERSION_TO_INSTALL_FLASK, MAP_VERSION_TO_INSTALL_XARRAY, MAP_VERSION_TO_INSTALL_MATPLOTLIB

def filter_instances(dataset_name, python_versions, constants):
    # Load the dataset
    dataset = load_dataset(dataset_name, split="test")
    
    # Extract repository and Python version mappings
    repo_python_versions = {}

    for repo, version_map in constants.items():
        for version, version_info in version_map.items():
            repo_version_key = f"{repo}:{version}"
            repo_python_versions[repo_version_key] = version_info['python']
        
    # Count the number of filtered instances per Python version
    version_counts: Dict[str, int] = {version: 0 for version in python_versions}
    instance_ids = []
    for instance in dataset:
        repo_version_key = f"{instance['repo']}:{instance['version']}"
        if repo_version_key not in repo_python_versions:
            continue
        if repo_python_versions[repo_version_key] in python_versions:
            version_counts[repo_python_versions[repo_version_key]] += 1
            instance_ids.append(instance['id'])
    
    return version_counts, instance_ids

# Define constants
DATASET_NAME = "kjain14/testgeneval"
PYTHON_VERSIONS = ["3.10"]
CONSTANTS = {
    "django/django": MAP_VERSION_TO_INSTALL_DJANGO,
    "psf/requests": MAP_VERSION_TO_INSTALL_REQUESTS,
    "scikit-learn/scikit-learn": MAP_VERSION_TO_INSTALL_SKLEARN,
    "pallets/flask": MAP_VERSION_TO_INSTALL_FLASK,
    "pydata/xarray": MAP_VERSION_TO_INSTALL_XARRAY,
    "matplotlib/matplotlib": MAP_VERSION_TO_INSTALL_MATPLOTLIB,
}

# Get counts of filtered instances
version_counts, ids = filter_instances(DATASET_NAME, PYTHON_VERSIONS, CONSTANTS)
print("Filtered Instance Counts:", version_counts)
with open("ids.txt", "w") as f:
    for id in ids:
        f.write(f"{id}\n")