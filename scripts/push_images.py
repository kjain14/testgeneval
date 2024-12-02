import os
import re
import subprocess
import argparse

# Function to parse the Makefile and extract image information
def parse_makefile(makefile_path):
    images = []
    docker_build_regex = re.compile(
        r'docker build .* -t (?P<image>[^\s]+) -f (?P<dockerfile>[^\s]+)'
    )

    with open(makefile_path, 'r') as f:
        for line in f:
            match = docker_build_regex.search(line)
            if match:
                images.append((match.group('image').replace("aorwall/", "kdjain/"), match.group('dockerfile')))
    return images

# Function to build, push, and optionally remove Docker images
def build_push_and_clean_images(images):
    for image, dockerfile in images:
        print(f"Building image: {image} using Dockerfile: {dockerfile}")
        try:
            # Build the image
            subprocess.run(['docker', 'build', '-t', image, '-f', dockerfile, '.'], check=True)
            if "bookworm-slim" in image:
                subprocess.run(['docker', 'build', '-t', image.replace("kdjain/", "aorwall/"), '-f', dockerfile, '.'], check=True)

            # Push the image
            print(f"Pushing image: {image}")
            subprocess.run(['docker', 'push', image], check=True)
            
            # Remove the image if it's not a base image
            if "bookworm-slim" not in image:
                print(f"Removing image: {image} to save space")
                subprocess.run(['docker', 'rmi', image], check=True)
            else:
                print(f"Skipping removal for base image: {image}")

        except subprocess.CalledProcessError as e:
            print(f"Error building, pushing, or removing image: {image}")
            print(e)
            continue

# Main script
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Build, push, and optionally clean Docker images based on a Makefile.")
    parser.add_argument("--makefile", default="Makefile.testgeneval", help="Path to the Makefile.")
    args = parser.parse_args()

    makefile_path = args.makefile
    if not os.path.exists(makefile_path):
        print(f"Makefile not found at {makefile_path}")
        exit(1)
    
    images = parse_makefile(makefile_path)
    if not images:
        print("No images found in the Makefile.")
        exit(1)

    build_push_and_clean_images(images)
