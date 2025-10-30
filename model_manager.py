from singleton import singleton
import logging
from pathlib import Path
from utils.terminal import run_command_in_terminal
@singleton
class ModelManager:
    """Singleton class to manage model configurations."""
    
    modelsMap = {
        "VOSK": {
            "fr": "vosk-model-fr-0.22",
            "en": "vosk-model-small-en-us-0.15",
        },
        "PIPER": {
            "fr": "fr_FR-tom-medium",
            "en": "piper-en_US-ryan-high",
        }
    }

    def __init__(self):
        self.models_directory = "models"
        self.language = "fr" # Default language
        logging.info("🧠 ModelManager initialized")
    
    def get_model_piper(self) -> str:
        """Get the Piper model name based on the selected language."""
        path = self.models_directory + "/" + "piper/" + self.modelsMap["PIPER"].get(self.language, "fr_FR-tom-medium")
        path += "/" + self.modelsMap["PIPER"].get(self.language, "fr_FR-tom-medium") + ".onnx"
        return path

    def get_model_vosk(self) -> str:
        """Get the VOSK model name based on the selected language."""
        path = self.models_directory + "/" + "vosk/" + self.modelsMap["VOSK"].get(self.language, "vosk-model-fr-0.22")
        return path
    
    def set_language(self, language: str):
        """Set the language for model selection."""
        if language in ["fr", "en"]:
            self.language = language
            logging.info(f"Language set to: {language}")
        else:
            raise ValueError("Unsupported language. Supported languages are 'fr' and 'en'.")
        
    def download_pipers_model(self):
        """Download the Piper model for the selected language."""
        from piper import download_voices
        model_name = self.modelsMap["PIPER"].get(self.language, "fr-tom-medium")
        download_dir = Path(self.models_directory + "/piper/" + model_name)
        download_dir.mkdir(parents=True, exist_ok=True)
        download_voices.download_voice(model_name, download_dir)
        print(f"Piper model '{model_name}' downloaded to '{download_dir}'")

    def download_vosk_model(self):
        """Download the VOSK model for the selected language."""
        import subprocess
        model_name = self.modelsMap["VOSK"].get(self.language, "vosk-model-fr-0.22")
        download_url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
        download_dir = Path(self.models_directory + "/vosk/")
        download_dir.mkdir(parents=True, exist_ok=True)
        zip_path = download_dir / f"{model_name}.zip"
        
        # Download the model zip file
        subprocess.run(["wget", "-O", str(zip_path), download_url], check=True)
        
        # Unzip the model
        subprocess.run(["unzip", "-o", str(zip_path), "-d", str(download_dir)], check=True)
        
        # Remove the zip file
        zip_path.unlink()
        
        print(f"VOSK model '{model_name}' downloaded and extracted to '{download_dir / model_name}'")

if __name__ == "__main__":
    ModelManager().set_language("fr")
    ModelManager().download_pipers_model()
    ModelManager().download_vosk_model()