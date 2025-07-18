from safetensors.torch import load_file
from tqdm.notebook import tqdm
import requests
import torch
import json
import os
import re

# Save urls.json
def save_param(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

# Load urls.json
def load_param(filename, load_type="load"):
    try:
        with open(filename, 'r') as f:
            params = json.load(f)
        return params
    except FileNotFoundError:
        if load_type == "load":
            return {
                "VAE": {
                    "keyname_to_url": {
                        "weight": {
                        },
                        "config": {
                        }
                    },
                    "url_to_keyname": {
                        "weight": {
                        },
                        "config": {
                        }
                    },
                    "hugging_face": [],
                },
                "Checkpoint": {
                    "keyname_to_url": {
                    },
                    "url_to_keyname": {
                    },
                    "hugging_face": [],
                },
                "LoRAs": {
                    "keyname_to_url": {
                    },
                    "url_to_keyname": {
                    },
                    "hugging_face": [],
                },
                "Embeddings": {
                    "keyname_to_url": {
                    },
                    "url_to_keyname": {
                    },
                    "hugging_face": [],
                },
            }
        elif load_type == "default":
            return {}

def default_model_for_checkpoint():
    return load_param("/content/StableDiffusionXLColabUI/json/default_models.json", load_type="default")

def inject_default(saved_urls, default):
    for key, value in default.items():
        saved_urls[key] = value
        
# Filter out any unsafe characters
def sanitize_filename(filename):
    name, ext = os.path.splitext(filename)
    safe_name = re.sub(r'[\\/:"*?<>.|]+', "_", name) # Replace all unsafe characters with underscores

    return safe_name + ext

# Check if the download is corrupt
def is_corrupt(path):
    try:
        if path.endswith(".safetensors"):
            tensor_check = load_file(path)
            _ = list(tensor_check.items())
            return False
        elif path.endswith((".bin", ".pth", ".ckpt")):
            _ = torch.load(path, map_location="cpu", weights_only=True)
            return False
        elif path.endswith(".json"):
            with open(path, "r") as f:
                _ = f.read()
            return False
            
    except Exception as e:
        print(e)
        return True

    return False 

# Search for a match
def search(type, name):
    for dir in os.listdir(f"/content/{type}"):
        if name in dir:
            return dir
    return name

# Check if a path exists
def is_exist(folder, name, type):
    if name.endswith(".safetensors") and not name.startswith(("https://", "http://", "/content")):
        subfolder, _ = os.path.splitext(name)
        weight_file = name
    elif name.startswith(("https://", "http://")):
        return False
    else:
        parts = name.strip("/").split("/")
        if len(parts) >= 2:
            subfolder = parts[-2]
            weight_file = parts[-1]
        else:
            subfolder = name
            weight_file = search(type, name)

    full_path = f"{folder}/{type}/{subfolder}" if type == "VAE" else f"{folder}/{type}/{weight_file}"

    if type == "VAE":
        try:
          return bool(os.listdir(full_path))
        except FileNotFoundError:
          return False
    if not os.path.exists(full_path):
        return False
    return True

def download(url, type, hf_token="", civit_token="", key=None, tqdm_bool=True, widget=None, esrgan=False):
    # Folder creation if not exist
    download_folder = f"/content/{type}" if not esrgan else type
    os.makedirs(download_folder, exist_ok=True)

    # Handling the url based on the given server
    if "civitai.com" in url:
        download_header = ""
        if civit_token:
            if "?" in url or "&" in url:
                download_url = f"{url}&token={civit_token}"
            else:
                download_url = url + f"token={civit_token}"
        else:
            download_url = url
    elif "huggingface.co" in url:
        if hf_token:
            download_header = {"Authorization": f"Bearer {hf_token}"}
        else:
            download_header = ""
        download_url = url
    else:
        download_header = ""
        download_url = url

    # Download
    if download_url and not is_exist(download_folder, url, type):
        if download_header:
            download_req = requests.get(download_url, headers=download_header, stream=True)
        else:
            download_req = requests.get(download_url, stream=True)

        # Request
        filename_content_disposition = download_req.headers.get("Content-Disposition")
        file_total_size = int(download_req.headers.get("content-length", 0))
        
        # Get the filename
        if filename_content_disposition:
            filename_find = re.search(r"filename=['\"]?([^'\"]+)['\"]?", filename_content_disposition)
            if filename_find:
                download_filename = sanitize_filename(filename_find.group(1))
            else:
                download_filename = sanitize_filename(os.path.basename(url) + ".safetensors") 
        else:
            download_filename = sanitize_filename(os.path.basename(url) + ".safetensors")

        full_path = f"{download_folder}/{download_filename}"

        # Return the full_path if exists
        if os.path.exists(full_path):
            return full_path
            
        # Download the file
        if tqdm_bool:
            with open(full_path, "wb") as f, tqdm(
                desc=download_filename,
                total=file_total_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in download_req.iter_content(chunk_size=1024):
                    f.write(chunk)
                    bar.update(len(chunk))
        else:
            with open(full_path, "wb") as f:
                downloaded = 0
                for chunk in download_req.iter_content(chunk_size=1024):
                    f.write(chunk)
                    downloaded += len(chunk)
                    widget.value = int((downloaded / file_total_size) * 100)

        # Return an empty string if the file is corrupted
        if is_corrupt(full_path):
            os.remove(full_path)
            return ""
            
    else:
        full_path = url

    # Return the path
    return full_path

# Validate if the url has been downloaded before (even in previous instance)
def download_file(url="", type="", hf_token="", civit_token="", base_path="", subfolder=None, tqdm=True, widget=None, update=False):
    # Load the dictionary from urls.json
    os.makedirs(f"{base_path}/Saved Parameters/URL", exist_ok=True)
    saved_urls = load_param(f"{base_path}/Saved Parameters/URL/urls.json")

    # Unused in the new version
    if "hugging_face" not in list(saved_urls["Checkpoint"].keys()):
        for key in list(saved_urls.keys()):
            saved_urls[key]["hugging_face"] = []

    # Default models
    default_model = default_model_for_checkpoint()
    if not all(
        item in list(saved_urls["Checkpoint"]["keyname_to_url"].keys()) for item in list(default_model["keyname_to_url"].keys())
    ):
        inject_default(saved_urls["Checkpoint"]["keyname_to_url"], default_model["keyname_to_url"])
        inject_default(saved_urls["Checkpoint"]["url_to_keyname"], default_model["url_to_keyname"])
        saved_urls["Checkpoint"]["hugging_face"] = saved_urls["Checkpoint"]["hugging_face"] + default_model["hugging_face"]

    if not update:
        # Get the values
        dict_type = saved_urls[type]
        os.makedirs(f"/content/{type}", exist_ok=True)
        
        # Select the key when loading VAE
        if subfolder:
            vae_key = "config"
        else:
            vae_key = "weight"
       
        # Handle URL input
        if url.startswith("https://") or url.startswith("http://"):
            key = dict_type.get("url_to_keyname").get(url) if type != "VAE" else dict_type.get("url_to_keyname").get(vae_key).get(url)
            if key:
                if is_exist(f"/content", key, type):
                    returned_path = f"/content/{type}/{search(type, key)}"
                else:
                    returned_path = download(url, type, hf_token, civit_token, tqdm_bool=tqdm, widget=widget)
            else:
                returned_path = download(url, type, hf_token, civit_token, tqdm_bool=tqdm, widget=widget)
                if type == "VAE":
                    if vae_key == "weight":
                        vae_name, _ = os.path.splitext(os.path.basename(returned_path))
                    elif vae_key == "config":
                        vae_name = subfolder
    
                    saved_urls[type]["url_to_keyname"][vae_key][url] = vae_name
                    saved_urls[type]["keyname_to_url"][vae_key][vae_name] = url
                else:
                    file_name, _ = os.path.splitext(os.path.basename(returned_path))
                    saved_urls[type]["url_to_keyname"][url] = file_name
                    saved_urls[type]["keyname_to_url"][file_name] = url
    
        # Unused, but can handle file from Google Drive
        elif url.startswith("/content/gdrive/MyDrive"):
            returned_path = url
    
        # Handle HF models
        elif url.count("/") == 1:
            returned_path = url
            if "hugging_face" not in saved_urls[type]:
                saved_urls[type]["hugging_face"] = []
            if url not in saved_urls[type]["hugging_face"]:
                saved_urls[type]["hugging_face"].append(url)
    
        # Handle key input
        else:
            key = url
            link = dict_type.get("keyname_to_url").get(key) if type != "VAE" else dict_type.get("keyname_to_url").get(vae_key).get(key)
            if link and not subfolder:
                if is_exist(f"/content", key, type):
                    returned_path = f"/content/{type}/{search(type, key)}"
                else:
                    returned_path = download(link, type, hf_token, civit_token, tqdm_bool=tqdm, widget=widget)
            elif subfolder:
                if is_exist(f"/content/VAE/{subfolder}", "config", type):
                    returned_path = f"/content/VAE/{subfolder}/config.json"
                else:
                    returned_path = download(link, type, hf_token, civit_token, tqdm_bool=tqdm, widget=widget)
            else:
                print(f"It seems like {url} doesn't exist in both /content/{type} directory and urls.json file. Is it a correct path?")
                returned_path = ""

    save_param(f"{base_path}/Saved Parameters/URL/urls.json", saved_urls)

    return returned_path if not update else None
