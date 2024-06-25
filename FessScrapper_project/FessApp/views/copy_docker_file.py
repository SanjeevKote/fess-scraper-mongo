import requests
import os
import tarfile
import io

def copy_file_from_container(container_id, src_path, dest_path):
    try:
        # Define Docker API endpoint
        docker_api = f"http://localhost:2375/containers/{container_id}/archive?path={src_path}"
        
        # Make the API request to get the file archive
        response = requests.get(docker_api, stream=True)
        
        if response.status_code == 200:
            # Create a temporary tar file in memory
            tar_data = io.BytesIO()
            for chunk in response.iter_content(chunk_size=4096):
                tar_data.write(chunk)
            
            tar_data.seek(0)
            
            # Extract the file from the tar archive
            with tarfile.open(fileobj=tar_data) as tar:
                member = tar.getmembers()[0]
                tar.extract(member, '/tmp')
                
                tmp_file = os.path.join('/tmp', member.name)
                
                # Move the temporary file to the desired location
                os.rename(tmp_file, dest_path)
                print(f"File copied to {dest_path}")
        else:
            print(f"Failed to get archive: {response.status_code} {response.text}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# copy_file_from_container('your_container_id', '/path/in/container', '/path/on/host')
