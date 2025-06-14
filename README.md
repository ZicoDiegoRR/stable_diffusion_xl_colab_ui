# Google Colab Non WebUI Stable Diffusion XL Image Generator

This is a simple Google Colab notebook made by an 18-years-old junior programmer for generating images using Stable Diffusion XL.

## Features
- **Image Generation:** Uses Transformers and Diffusers as the major components for image generation, along with ControlNet, Inpainting, and IP-Adapter.
- **Download and Load:** Ability to download and load images, checkpoint, LoRA weights, and VAE using direct URLs.
- **Textual Inversion:** Ability to load embeddings for more output control. 
- **Image-to-Image:** Turn your images into something more creative and unique. 
- **Prompt Generator:** Generate creative prompt powered by GPT-2. (Model by [Gustavosta](https://huggingface.co/Gustavosta))
- **Image Upscaling:** Using [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) made by [xinntao](https://github.com/xinntao) and Real-ESRGAN's contributors. 
- **Google Drive Integration:** Can connect to your Google Drive or disable it.
- **User-Friendly UI:** Simplified complexity with an easy-to-understand user interface.
- **IPyWidgets:** Simplified UI so that you don't need to scroll up and down. 
- **Built-in History System:** Can show all of your previously generated images in Google Drive without opening it, just with a few simple clicks.
- **Preset System:** Enables saving, loading, renaming, and deleting presets containing your saved parameters.
- **CivitAI Token Support:** Pass your CivitAI token for additional functionality, but remember **never share it with anyone.**
- **Hugging Face Token Support:** Pass your Hugging Face token for accessing private files, but remember **never share it with anyone.**
- **Simplicity:** Consists of two cells only.

> [!IMPORTANT]\
> With the current update, the Inpainting feature is under development and it may fail. Please use the older version in the "Legacy" branch if you wish to use Inpainting.

## Usage
This notebook is designed for artistic purposes and to spark inspiration. **Please use it responsibly.** Creating deepfakes and uploading them online are strictly prohibited.

## Installation
Simply open the notebook on Google Colab to start using it. No installation is needed. 

**Link:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ZicoDiegoRR/stable_diffusion_xl_colab_ui/blob/main/V3.ipynb)

> [!NOTE]\
> Check out the [Legacy branch](https://github.com/ZicoDiegoRR/stable_diffusion_xl_colab_ui/tree/legacy) to use the old versions of this notebook.

## Disclaimer
- This tool is intended for creating art and exploring creative image generation.
- **Use responsibly.** Please refrain from using it for any malicious or harmful activities.
- NSFW generation is supported, but do it at your own risk.

## Feature Table
<details> <summary>Click here</summary>
  
|     | Features                                                                                                                     |
|-----|------------------------------------------------------------------------------------------------------------------------------|
| 1.  | Base pipelines and autoencoder (ControlNetUnion, Inpainting, VAE, Text2Img)                                                  |
| 2.  | Base adapters (LoRA, IP-Adapter)                                                                                             |
| 3.  | IPyWidgets                                                                                                                   |
| 4.  | Saving and loading parameters                                                                                                |
| 5.  | Interactive UI                                                                                                               |
| 6.  | Linking widgets                                                                                                              |
| 7.  | History system                                                                                                               |
| 8.  | Upload images directly                                                                                                       |
| 9.  | Image-to-image                                                                                                               |
| 10. | Textual inversion or embeddings                                                                                              |
| 11. | Send images from history to Image-to-image, ControlNet, Inpainting, and/or IP-Adapter                                        |
| 12. | Reset button (defaulting the parameters)                                                                                     |
| 13. | Compatibility with saved parameters from previous versions                                                                   |
| 14. | Preset system (saving and loading custom parameters)                                                                         |
| 15. | GPT-2 Prompt Generator                                                                                                       |
| 16. | Hugging Face token integration                                                                                               |
| 17. | Real-ESRGAN Image Upscaling                                                                                                  |
| 18. | New parameters saving system (from a flat list to a dictionary) and a conversion method to convert old saves to the new ones |
| 19. | URL saving system to save any previously-inputted URLs into a JSON file and access them with filenames only                  |
| 20. | Preview buttons to display ControlNet's converted image                                                                      |
| 21. | `components` integration for memory-sharing between pipelines to avoid OutOFMemory error due to independent tensors          |

</details>

## Preview
Work in progress

## To-do List
- Adding textual inversion ✅ 
- Implementing Inpainting using IPyCanvas
- Creating the UI preview
- Modularizing the code (testing)
- Overhauling the save system ✅
- Adding Hugging Face's token integration ✅ 
- Implementing Img2Img pipeline ✅ 
## License
This project is open-source and free to use under the MIT License.

---

This README was partially made by ChatGPT.
