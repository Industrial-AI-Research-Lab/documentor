"""Example usage of Qwen2.5-VL specific methods."""

from PIL import Image

from .config import OCRPipelineConfig
from .qwen_client import QwenClient


def demonstrate_qwen_methods(image_path: str) -> None:
    """Demonstrate word detection and text recognition with Qwen2.5-VL."""
    
    # Load image
    image = Image.open(image_path)
    
    # Create Qwen client
    config = OCRPipelineConfig.create_default()
    qwen_client = QwenClient(config.qwen_config)
    
    print("=== Word Detection ===")
    try:
        words = qwen_client.detect_words(image)
        print(f"Detected {len(words)} words:")
        for word in words:
            print(f"  Word: {word['word']}")
            print(f"  Bbox: {word['bbox']}")
            print(f"  Confidence: {word['confidence']}")
            print("  ---")
    except Exception as e:
        print(f"Word detection failed: {e}")
    
    print("\n=== Text Recognition ===")
    try:
        text = qwen_client.recognize_text(image)
        print(f"Recognized text:\n{text}")
    except Exception as e:
        print(f"Text recognition failed: {e}")


if __name__ == "__main__":
    # Example usage
    demonstrate_qwen_methods("example.pdf")
