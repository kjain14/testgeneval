import argparse
import subprocess
import os
import shutil
from datasets import load_dataset
from concurrent.futures import ThreadPoolExecutor

def read_ids_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            ids = [line.strip() for line in file if line.strip()]
        return ids
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def generate_docker_image(curr_id):
    return f"kdjain/sweb.eval.x86_64.{curr_id.rsplit('-', 1)[0].replace('__', '_s_')}"

def prepare_output_dir(output_base_dir, image_name):
    sanitized_image_name = image_name.replace("/", "_").replace(":", "_")
    output_dir = os.path.join(output_base_dir, sanitized_image_name)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def run_pynguin_in_docker(image, instance, output_dir):
    try:
        if '/' in instance['code_file']:
            instance_dir = instance['code_file'].rsplit('/', 1)[0]
        else:
            instance_dir = ""

        instance_module = instance['code_file'].replace(".py", "").replace("/", ".")

        print(f"Running pynguin in Docker image: {image}")
        docker_command = [
            "docker", "run", "--rm", 
            "-e", "PYNGUIN_DANGER_AWARE=1",
            "-v", f"{os.path.abspath(output_dir)}:/output",
            image,
            "bash", "-c", 
            f"source activate testbed && pip install git+https://github.com/kjain14/pynguin &&"
            f"pynguin --maximum-test-execution-timeout 30 --test-execution-time-per-statement 30 --maximum_search_time 600 --project-path /testbed/{instance_dir} --output-path /output --module-name {instance_module} -v"
        ]

        process = subprocess.run(docker_command, check=False, timeout=3600)
        
        if process.returncode != 0:
            print(f"Error: Command failed with return code {process.returncode}.")
    
    except subprocess.TimeoutExpired:
        print("Error: Docker command took longer than 30 minutes. Skipping this run...")
            
    except subprocess.CalledProcessError as e:
        print(f"Error running pynguin in Docker image {image}:\n{e}")

def process_instance(instance, output_base_dir):
    image = generate_docker_image(instance['id'])
    output_dir = prepare_output_dir(output_base_dir, instance['id'])
    if os.path.exists(output_dir):
        has_py_file = any(file.endswith('.py') for file in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, file)))

        if has_py_file:
            return

    run_pynguin_in_docker(image, instance, output_dir)
    os.system("docker system prune -f")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run pynguin in Docker containers and capture outputs."
    )
    parser.add_argument("--input_file", help="Path to the input file containing IDs", required=True)
    parser.add_argument("--dataset", help="Name of dataset", default="kjain14/testgeneval")
    parser.add_argument("--output_base_dir", help="Base directory to store pynguin outputs", required=True)
    
    args = parser.parse_args()

    ids = read_ids_from_file(args.input_file)
    dataset = load_dataset(args.dataset, split="test")
    dataset = dataset.filter(lambda instance: instance['id'] in ids)

    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [
            executor.submit(process_instance, instance, args.output_base_dir)
            for instance in dataset
        ]
        for future in futures:
            future.result()

    print("Pynguin execution completed for all Docker images.")
