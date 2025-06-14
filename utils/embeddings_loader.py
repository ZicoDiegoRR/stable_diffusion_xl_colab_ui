from StableDiffusionXLColabUI.utils import downloader
from safetensors.torch import load_file
import re
import os

def load_textual_inversion_from_link(pipe, link, token, name):
    # Loading one by one
    for embed, tag, name in zip(link, token, name):
        try:
            ti_dict = load_file(embed)
            print(f"Loading {name}...")
            pipe.load_textual_inversion(ti_dict["clip_g"], token=tag, text_encoder=pipe.text_encoder_2, tokenizer=pipe.tokenizer_2)
            pipe.load_textual_inversion(ti_dict["clip_l"], token=tag, text_encoder=pipe.text_encoder, tokenizer=pipe.tokenizer)
        except Exception as e:
            print(f"Skipped {name}. Reason: {e}")
    
def download_textual_inversion(pipe, link, token, widget, hf_token, civit_token, base_path):
    # Download and handle duplication
    ti_list = []
    ti_path = []
    tokens = []
    unique_ti_urls = []
    
    for i, url in enumerate(link):
        textual_inversion_path = ""
        if url not in unique_ti_urls:
            if url.startswith("https://") or url.startswith("http://"):
                textual_inversion_path = downloader.download_file(url, "Embeddings", hf_token, civit_token, base_path)
            else:
                if url.startswith("/content/LoRAs/"):
                    ti_check = os.path.basename(url)
                else:
                    ti_check = url
                textual_inversion_path = downloader.download_file(url, "Embeddings", hf_token, civit_token, base_path)

            if textual_inversion_path:
                unique_ti_urls.append(url)
                ti_path.append(textual_inversion_path)

                split_filename, _ = os.path.splitext(os.path.basename(textual_inversion_path))
                ti_list.append(split_filename)
                tokens.append(token[i])

                widget_value = widget.value.replace(url, split_filename)
                widget.value = widget_value
            else:
                print(f"It seems like {url} is an invalid path or doesn't exist. Make sure to put a correct path to ensure the weight being loaded correctly.")
                print(f"Skipped {url}.")

    load_textual_inversion_from_link(pipe, ti_path, tokens, ti_list)
        
def process(pipe, link, token, widget, hf_token, civit_token, base_path):
    # Preprocessing the urls and weight before downloading
    ti_links = [word for word in re.split(r"\s*,\s*", link)]
    ti_tokens = [word for word in re.split(r"\s*,\s*", token)]
    
    os.makedirs("/content/Embeddings", exist_ok=True)

    download_textual_inversion(pipe, ti_links, ti_tokens, widget, hf_token, civit_token, base_path)

