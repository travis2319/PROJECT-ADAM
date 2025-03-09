import os
import requests  # type: ignore

def upload_to_server(file_path, server_url):
    """Upload the file to a remote server"""
    try:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist")
            return False
            
        print(f"Uploading {file_path} to {server_url}...")
        
        # Prepare the file for upload
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file, 'text/csv')}
            
            # Send POST request to the server
            response = requests.post(server_url, files=files)
            
            # Check if upload was successful
            if response.status_code == 200:
                print(f"Upload successful! Server response: {response.text}")
                return True
            else:
                print(f"Upload failed. Status code: {response.status_code}")
                print(f"Server response: {response.text}")
                return False
                
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False