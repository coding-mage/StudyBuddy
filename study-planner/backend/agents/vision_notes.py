class VisionNotesAgent:
    def run(self, payload):
        try:
            import pytesseract
            from PIL import Image
            img = Image.open(payload["image_path"])
            text = pytesseract.image_to_string(img)
        except Exception as e:
            print(f"VisionNotes OCR load failed: {e}. Falling back to mock extracted text.")
            text = "Mock extracted notes: [OCR fell back because Tesseract/Pillow is not running on the server. Please run locally for full features.]"

        return {
            "type": "markdown_notes",
            "content": f"## Digitized Notes\n\n{text}"
        }
