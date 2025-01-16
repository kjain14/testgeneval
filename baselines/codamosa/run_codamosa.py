import argparse
import subprocess
import os
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
    """
    sanitized_image_name = image_name.replace("/", "_").replace(":", "_")
    output_dir = os.path.abspath(os.path.join(output_base_dir, sanitized_image_name))
        
    os.makedirs(output_dir, exist_ok=True)  # Create a fresh directory
    return output_dir

def run_codamosa_in_docker(image, instance, output_dir):
    """
    Run CoDAMOSA inside a Docker container and capture test cases.
    """
    try:
        if '/' in instance['code_file']:
            instance_dir = instance['code_file'].rsplit('/', 1)[0]
        else:
            instance_dir = ""

        instance_module = instance['code_file'].replace(".py", "").replace("/", ".")

        print(f"Running CoDAMOSA in Docker image: {image}")
        docker_command = [
            "docker", "run", "--rm", 
            "-v", f"{output_dir}:/output",  # Mount local output directory
            "-v", f"{output_dir}/testbed:/input:ro",
            "-v", f"{output_dir}/testbed:/package:ro",
            "codamosa-runner",
            "--project_path", "/input",
            "--module-name", instance_module,
            "--output-path", "/output",
            "--report-dir", "/output",
            "--maximum_search_time", "600",
            "--output_variables", "TargetModule,CoverageTimeline",
            "--coverage_metrics", "BRANCH,LINE",
            "--algorithm", "CODAMOSA",
            "--model_base_url", "https://api.openai.com/v1",
            "--model_relative_url", "/chat/completions",
            "-v",
            "--include-partially-parsable", "True",
            "--allow-expandable-cluster", "True",
            "--uninterpreted_statements", "ONLY",
            "--temperature", "0.2",
            "--model_name", "gpt-4o",
            "--authorization-key", os.environ.get("AUTH_KEY"),
        ]

        # Run Docker command and print output directly
        process = subprocess.run(docker_command, check=False)
        if process.returncode != 0:
            print(f"Error: Command failed with return code {process.returncode}.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running CoDAMOSA in Docker image {image}: {e}")

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Run CoDAMOSA in Docker containers and capture outputs."
    )
    parser.add_argument("--input_file", help="Path to the input file containing IDs", required=True)
    parser.add_argument("--dataset", help="Name of dataset", default="kjain14/testgeneval")
    parser.add_argument("--output_base_dir", help="Base directory to store CoDAMOSA outputs", required=True)
    
    args = parser.parse_args()

    # Read IDs and generate Docker images
    ids = read_ids_from_file(args.input_file)
    dataset = load_dataset(args.dataset, split="test")
    
    dataset = dataset.filter(lambda instance: instance['id'] in ids)
    # Run CoDAMOSA for each image
    for instance in dataset:
        image = generate_docker_image(instance['id'])
        output_dir = prepare_output_dir(args.output_base_dir, instance['id'])
        if os.path.exists(output_dir):
            has_py_file = any(file.endswith('.py') for file in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, file)))
            if has_py_file:
                continue

        run_codamosa_in_docker(image, instance, output_dir)
        os.system("docker system prune -f")

    print("CoDAMOSA execution completed for all Docker images.")
