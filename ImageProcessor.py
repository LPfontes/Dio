from PIL import Image

class ImageProcessor:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path).convert("RGB")  # Converte para RGB ao abrir

    def resize(self, width, height):
        self.image = self.image.resize((width, height))

    def save(self, output_path):
        self.image.save(output_path, format='WEBP')  # Salva em formato WEBP