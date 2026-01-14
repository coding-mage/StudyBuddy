import pytesseract
from PIL import Image

class VisionNotesAgent:
    def run(self, payload):
        img = Image.open(payload["image_path"])
        text = pytesseract.image_to_string(img)

        return {
            "type": "markdown_notes",
            "content": f"## Digitized Notes\n\n{text}"
        }
