import ipywidgets as widgets
import json
import re

def load_param(filename):
    try:
        with open(filename, 'r') as f:
            params = json.load(f)
        return params
    except FileNotFoundError:
        return {}

class LoRALoader:
    def collect_values(self): # Function to return the value
        self.lora_urls_widget.value, self.weight_scale_widget.value = self.read()
        return [self.lora_urls_widget.value, self.weight_scale_widget.value]

    def wrap_settings(self): # Function to collect every widget into a vbox for convenience
        return self.lora_settings

    def return_widgets(self):
        return [
            self.lora_urls_widget,
            self.weight_scale_widget
        ]

    def refresh_model(self):
        saved_models = load_param(f"{self.base_path}/Saved Parameters/URL/urls.json").get("LoRAs")
        saved_hf_models = saved_models["hugging_face"] if saved_models and "hugging_face" in saved_models else []
        if not saved_models:
            model_options = []
        else:
            model_options = list(saved_models["keyname_to_url"].keys())
        return model_options + saved_hf_models
        
    def lora_click(self, link, scale, construct=False): # Function to add widgets after clicking the plus button
        lora_url_input = widgets.Combobox(value=link, options=self.refresh_model(), placeholder="Input the link here", description="Weight file", ensure_option=False)
        lora_scale_input = widgets.FloatSlider(value=scale, min=-5, max=5, step=0.1, description="Weight Scale")
        lora_remove_button = widgets.Button(description="X", button_style='danger', layout=widgets.Layout(width='30px', height='30px'))

        if construct and not self.lora_construct_bool:
            self.lora_nested_vbox.children = []
            self.lora_construct_bool = True
            
        self.lora_nested_vbox.children += (lora_url_input, lora_scale_input, lora_remove_button, )
        lora_remove_button.on_click(
            lambda b: self.lora_remover(
                list(self.lora_nested_vbox.children).index(lora_remove_button) - 2, 
                list(self.lora_nested_vbox.children).index(lora_remove_button) - 1, 
                list(self.lora_nested_vbox.children).index(lora_remove_button)
            )
        )
        self.lora_settings.children = [self.lora_add, self.lora_nested_vbox]

    def read(self): # Function to process every value from the widgets into two strings to be fed into the main logic 
        collected_lora_urls = ""
        collected_lora_scales = ""
        for i in range(len(self.lora_nested_vbox.children)):
            if i % 3 == 0:
                if self.lora_nested_vbox.children[i].value != "":
                    collected_lora_urls += (self.lora_nested_vbox.children[i].value + ",")
            elif i % 3 == 1:
                if self.lora_nested_vbox.children[i - 1].value != "":
                    collected_lora_scales += (str(self.lora_nested_vbox.children[i].value) + ",")
        return collected_lora_urls.rstrip(","), collected_lora_scales.rstrip(",")

    def lora_remover(self, link, scale, remove_button): # Function to remove lora (only the widgets, not the actual file)
        lora_nested_list = list(self.lora_nested_vbox.children)
        lora_nested_list.pop(remove_button)
        lora_nested_list.pop(scale)
        lora_nested_list.pop(link)
        self.lora_nested_vbox.children = tuple(lora_nested_list)

    def construct(self, cfg): # Function to add widgets based on pre-existing URLs from the saved parameter
        lora_links = re.split(r"\s*,\s*", self.lora_urls_widget.value)
        lora_scales = re.split(r"\s*,\s*", self.weight_scale_widget.value)
        for lora, scale in zip(lora_links, lora_scales):
            if lora:
                self.lora_click(lora, float(scale), construct=True)
        self.lora_construct_bool = False

    def __init__(self, cfg, base_path):
        self.base_path = base_path
        
        self.lora_urls_widget = widgets.Text(value=cfg[0] if cfg else "")
        self.weight_scale_widget = widgets.Text(value=cfg[1] if cfg else "")

        self.lora_add = widgets.Button(description="+", button_style='success', layout=widgets.Layout(width='30px', height='30px'))
        self.lora_nested_vbox = widgets.VBox()
        self.lora_settings = widgets.VBox([self.lora_add])

        self.lora_construct_bool = False

        self.lora_add.on_click(lambda b: self.lora_click("", 1.0))
        self.construct(cfg)
