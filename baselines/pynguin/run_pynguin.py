import argparse
import subprocess
import os
import shutil
from datasets import load_dataset

def read_ids_from_file(file_path):
    """
    Reads a file line by line and extracts IDs.
    """
    try:
        with open(file_path, 'r') as file:
            ids = [line.strip() for line in file if line.strip()]
        return ids
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def generate_docker_image(curr_id):
    """
    Generate Docker image names based on ID.
    """
    return f"kdjain/sweb.eval.x86_64.{curr_id.rsplit('-', 1)[0].replace('__', '_s_')}"

def prepare_output_dir(output_base_dir, image_name):
    """
    Prepare a clean output directory for each Docker image.
    :param output_base_dir: Base directory for all outputs.
    :param image_name: Docker image name to create a subdirectory.
    :return: Path to the cleaned subdirectory.
    """
    sanitized_image_name = image_name.replace("/", "_").replace(":", "_")
    output_dir = os.path.join(output_base_dir, sanitized_image_name)
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  # Clean up old output
    
    os.makedirs(output_dir)  # Create a fresh directory
    return output_dir

def run_pynguin_in_docker(image, instance, output_dir):
    """
    Run pynguin inside a Docker container and capture test cases.
    :param image: Docker image name.
    :param instance_file: Path to the instances file in Docker (/testbed).
    :param output_dir: Directory to save pynguin outputs locally.
    """
    try:
        if '/' in instance['code_file']:
            instance_dir = instance['code_file'].rsplit('/', 1)[0]
        else:
            instance_dir = ""

        instance_module = instance['code_file'].replace(".py", "").replace("/", ".")

        print(f"Running pynguin in Docker image: {image}")
        docker_command = [
            "docker", "run", "--rm", 
            "-e", "PYNGUIN_DANGER_AWARE=1",  # Required for pynguin to run
            "-v", f"{os.path.abspath(output_dir)}:/output",  # Mount local output directory
            image,
            "bash", "-c", 
            f"source activate testbed && pip install git+https://github.com/kjain14/pynguin &&"
            f"pynguin --maximum-iterations 25 --project-path /testbed/{instance_dir} --output-path /output --module-name {instance_module} -v"
        ]

        
        # Run Docker command and print output directly
        process = subprocess.run(docker_command, check=False)
        if process.returncode != 0:
            print(f"Error: Command failed with return code {process.returncode}.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running pynguin in Docker image {image}:\n{e}")

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Run pynguin in Docker containers and capture outputs."
    )
    parser.add_argument("--input_file", help="Path to the input file containing IDs", required=True)
    parser.add_argument("--dataset", help="Name of dataset", default="kjain14/testgeneval")
    parser.add_argument("--output_base_dir", help="Base directory to store pynguin outputs", required=True)
    
    args = parser.parse_args()

    # Read IDs and generate Docker images
    ids = read_ids_from_file(args.input_file)
    dataset = load_dataset(args.dataset, split="test")
    
    dataset = dataset.filter(lambda instance: instance['id'] in ids)
    # Run pynguin for each image
    for instance in dataset:
        image = generate_docker_image(instance['id'])
        output_dir = prepare_output_dir(args.output_base_dir, instance['id'])
        run_pynguin_in_docker(image, instance, output_dir)
        os.system("docker system prune")

    print("Pynguin execution completed for all Docker images.")
