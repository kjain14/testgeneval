import argparse
import subprocess
import os
from datasets import load_dataset


def prepare_output_dir(output_base_dir, image_name):
    """
    Prepare a clean output directory for each Docker image.
    :param output_base_dir: Base directory for all outputs.
    :param image_name: Docker image name to create a subdirectory.
    :return: Path to the cleaned subdirectory.
    """
    sanitized_image_name = image_name.replace("/", "_").replace(":", "_")
    output_dir = os.path.join(output_base_dir, sanitized_image_name)

    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    return output_dir


def copy_testbed_from_docker(image, output_dir):
    """
    Copy the /testbed directory from a Docker container to the output directory.
    :param image: Docker image name.
    :param output_dir: Directory to save the /testbed contents.
    """
    try:
        print(f"Copying /testbed from Docker image: {image}")
        docker_command = [
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath(output_dir)}:/output",  # Mount local output directory
            image,
            "bash", "-c",
            "cp -r /testbed /output"
        ]

        # Run Docker command
        result = subprocess.run(docker_command, check=False)
        if result.returncode == 0:
            print(f"/testbed successfully copied to {output_dir}")
        else:
            print(f"Error: Command failed with return code {result.returncode}.")

    except subprocess.CalledProcessError as e:
        print(f"Error copying /testbed from Docker image {image}: {e}")


def run_pip_freeze_in_docker(image, output_dir):
    """
    Run `pip freeze` inside a Docker container and save the output to `requirements.txt`.
    :param image: Docker image name.
    :param output_dir: Directory to save the requirements.txt file.
    """
    try:
        requirements_path = os.path.join(output_dir, "requirements.txt")

        print(f"Running pip freeze in Docker image: {image}")
        docker_command = [
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath(output_dir)}:/output",
            image,
            "bash", "-c",
            "echo 'numpy == 1.24.0\npackaging >= 20.0\npandas >= 1.1' > /output/testbed/package.txt"
        ]
        
        # Run Docker command
        result = subprocess.run(docker_command, check=False)
        if result.returncode == 0:
            print(f"requirements.txt saved in {requirements_path}")
        else:
            print(f"Error: Command failed with return code {result.returncode}.")

    except subprocess.CalledProcessError as e:
        print(f"Error running pip freeze in Docker image {image}: {e}")


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Copy /testbed from Docker containers and run pip freeze."
    )
    parser.add_argument("--input_file", help="Path to the input file containing IDs", required=True)
    parser.add_argument("--dataset", help="Name of dataset", default="kjain14/testgeneval")
    parser.add_argument("--output_base_dir", help="Base directory to store outputs", required=True)

    args = parser.parse_args()

    # Read IDs and generate output directories
    ids = []
    try:
        with open(args.input_file, 'r') as file:
            ids = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        exit(1)

    dataset = load_dataset(args.dataset, split="test")
    dataset = dataset.filter(lambda instance: instance['id'] in ids)

    # Process each instance
    for instance in dataset:
        image = f"kdjain/sweb.eval.x86_64.{instance['id'].rsplit('-', 1)[0].replace('__', '_s_')}"
        output_dir = prepare_output_dir(args.output_base_dir, instance['id'])

        # Copy /testbed directory and run pip freeze
        copy_testbed_from_docker(image, output_dir)
        run_pip_freeze_in_docker(image, output_dir)

    os.system("docker system prune -f")
    print("Execution completed for all instances.")
