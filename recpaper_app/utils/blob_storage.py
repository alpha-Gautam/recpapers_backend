import os
import json
import requests
import uuid
import mimetypes
from urllib.parse import urlparse, quote
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
import vercel_blob

@deconstructible
class VercelBlobStorage(Storage):
    def __init__(self):
        self.blob_token = os.environ.get("BLOB_READ_WRITE_TOKEN")
        if not self.blob_token:
            from django.conf import settings
            self.blob_token = getattr(settings, "BLOB_READ_WRITE_TOKEN", None)
            
        if not self.blob_token:
            raise Exception("BLOB_READ_WRITE_TOKEN not set in environment variables or settings")
            
        self.put_base_url = "https://blob.vercel-storage.com"

    def _save(self, name, content):
        pathname = quote(name)

        content.seek(0)
        file_content = content.read()
        content_length = len(file_content)

        content_type, _ = mimetypes.guess_type(name)
        if content_type is None:
            content_type = 'application/octet-stream'

        api_version = "6"
        upload_url = f"{self.put_base_url}/{pathname}?x-api-version={api_version}"

        headers = {
            "Authorization": f"Bearer {self.blob_token}",
            "Content-Type": content_type,
            "x-content-length": str(content_length),
        }
        
        try:
            response = requests.put(
                upload_url,
                headers=headers,
                data=file_content
            )
            
            if response.status_code == 200:
                response_data = response.json()
                return response_data['url'] 
            else:
                error_message = f"Failed to upload to Vercel Blob. Status: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_message += f", Detail: {json.dumps(error_detail)}"
                except json.JSONDecodeError:
                    error_message += f", Response: {response.text}"
                
                print(f"Upload Error - Status: {response.status_code}, URL: {upload_url}, Headers: {headers}")
                print(f"Response body: {response.text}")
                raise Exception(error_message)
        except requests.exceptions.RequestException as e:
            raise Exception(f"RequestException during Vercel Blob upload: {str(e)}")
        except Exception as e:
            raise Exception(f"Generic error during Vercel Blob upload: {str(e)}")
    
    def _open(self, name, mode='rb'):
        response = requests.get(name) 
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve file from {name}: {response.status_code} - {response.text}")
        
        parsed_url = urlparse(name)
        filename = os.path.basename(parsed_url.path)
        return ContentFile(response.content, name=filename)
    
    def delete(self, name):
        """
        Delete a file from Vercel Blob storage.
        'name' is the full URL of the blob to delete.
        """
        # Extract pathname from URL
        parsed_url = urlparse(name)
        pathname = parsed_url.path
        
        # Remove leading slash if present
        if pathname.startswith('/'):
            pathname = pathname[1:]
        
        api_version = "6"
        delete_url = f"{self.put_base_url}/delete"
        
        headers = {
            "Authorization": f"Bearer {self.blob_token}",
            "Content-Type": "application/json",
            "x-api-version": api_version
        }
        
        # According to Vercel Blob API, we need to send the pathname in the request body
        payload = {
            "pathname": pathname
        }
        
        # For debugging
        print(f"Attempting to delete blob from {name}")
        print(f"Extracted pathname: {pathname}")
        print(f"Delete URL: {delete_url}")
        
        try:
            response = requests.post(
                delete_url,
                headers=headers,
                json=payload
            )
            
            print(f"Delete response status: {response.status_code}")
            try:
                response_body = response.json()
                print(f"Delete response body: {json.dumps(response_body)}")
            except json.JSONDecodeError:
                print(f"Delete response text: {response.text}")
            
            if response.status_code in [200, 204]:
                print(f"Successfully deleted {name} from Vercel Blob")
                return True
            else:
                error_message = f"Failed to delete {name}, status: {response.status_code}"
                print(error_message)
                # Important: We need to raise an exception to prevent Django from silently ignoring the failure
                raise Exception(error_message)
        except requests.exceptions.RequestException as e:
            error_message = f"Request error deleting blob: {str(e)}"
            print(error_message)
            raise Exception(error_message)
        except Exception as e:
            error_message = f"Error deleting blob: {str(e)}"
            print(error_message)
            raise Exception(error_message)
    
    def exists(self, name):
        try:
            response = requests.head(name)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def url(self, name):
        return name
    
    def size(self, name):
        try:
            response = requests.head(name)
            response.raise_for_status() 
            return int(response.headers.get('content-length', 0))
        except requests.exceptions.RequestException:
            return 0

def upload_to_blob(file_obj, filename=None):
    storage = VercelBlobStorage()
    name_to_save = filename or getattr(file_obj, 'name', 'unknown_file')
    if isinstance(file_obj, bytes):
        content = ContentFile(file_obj, name_to_save)
    else:
        content = file_obj
    return storage._save(name_to_save, content)

def delete_from_blob(url):
    storage = VercelBlobStorage()
    storage.delete(url)
    return True