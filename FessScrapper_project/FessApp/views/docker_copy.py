import subprocess

def docker_copy_from_container(container_name, container_path, local_path):
    try:
        # Construct the docker cp command
        command = f"docker cp {container_name}:{container_path} {local_path}"
        
        # Execute the command
        subprocess.run(command, check=True, shell=True)
        
        print(f"Successfully copied {container_path} from {container_name} to {local_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during docker cp: {e}")

# def main():
#     container_name = "fess-scrapper-api"
#     container_path = full_path
#     local_path = "/tmp"
    
#     # Call the function to copy the file
#     docker_copy_from_container(container_name, container_path, local_path)

# if __name__ == "__main__":
#     main()
