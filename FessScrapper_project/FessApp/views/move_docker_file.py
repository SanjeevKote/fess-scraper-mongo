import docker
import paramiko
import os
import tarfile
import io


def move_file_from_container(container_id, source_path, destination_path):
    # Docker client
    # client = docker.DockerClient(base_url='tcp://localhost:2375')
 # Create a Docker client
    client = docker.from_env()
    
    # Find the container by name
    container = client.containers.get(container_id)

    # Copy the file from the container to the local path
    bits, stat = container.get_archive(source_path)
    
    # Extract the tar stream
    file_like_object = io.BytesIO()
    for chunk in bits:
        file_like_object.write(chunk)
    file_like_object.seek(0)
    
    with tarfile.open(fileobj=file_like_object) as tar:
        member = tar.getmember(os.path.basename(source_path))
        file_content = tar.extractfile(member).read()
    
    # Write the extracted file to the local path
    with open(destination_path, 'wb') as file:
        file.write(file_content)
    
    print(f"File copied from container to local path: {destination_path}")

        

# Call the function to copy the file
#copy_file_from_container(container_id, source_path, destination_path)
