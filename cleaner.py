import time
import os
import subprocess

# def is_image_in_use(image_id):
#     """Check if an image is being used by any running or stopped containers."""
#     result = subprocess.run(
#         ["docker", "ps", "-a", "--format", "{{.Image}}"],
#         capture_output=True, text=True
#     )
#     used_images = result.stdout.strip().split("\n")
    
#     return image_id in used_images  # True if the image is in use

# def remove_images_with_prefix(prefix):
#     # Get list of images with their IDs and repositories
#     result = subprocess.run(
#         ["docker", "images", "--format", "{{.Repository}} {{.ID}}"],
#         capture_output=True, text=True
#     )

#     images = result.stdout.strip().split("\n")

#     for image_info in images:
#         if not image_info.strip():
#             continue
#         repo, image_id = image_info.rsplit(" ", 1)  # Extract repo and ID
#         if repo.startswith(prefix):
#             if is_image_in_use(image_id):
#                 print(f"Skipping image {repo} ({image_id}) - it is in use.")
#             else:
#                 print(f"Removing image {repo} ({image_id})...")
#                 os.system(f"docker rmi -f {image_id}")

if __name__ == "__main__":
    while True:
        os.system("echo y | docker system prune -a")
        time.sleep(600)