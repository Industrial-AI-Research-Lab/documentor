"""Example usage of OCR pipeline."""

from PIL import Image

from .config import OCRPipelineConfig
from .pdf_processor import PDFProcessor
from .detector import DotsBlockDetector
from .recognizer import QwenBlockRecognizer
from .dots_ocr_client import DotsOCRClient
from .qwen_client import QwenClient
from .pipeline import ScanPipeline


def process_pdf(pdf_path: str, page_image: Image.Image, page_num: int = 0) -> None:
    """Process PDF page with selectable text support."""
    
    # Create configuration
    config = OCRPipelineConfig.create_default()
    
    # Create PDF processor
    processor = PDFProcessor(config)
    
    # Process PDF page
    fragments = processor.process_pdf_page(pdf_path, page_image, page_num)
    
    # Print results
    for fragment in fragments:
        print(f"Type: {type(fragment).__name__}")
        print(f"Value: {fragment.value}")
        print(f"Style: {fragment.style}")
        print("---")


def process_image(image_path: str) -> None:
    """Process image using OCR pipeline."""
    
    # Load image
    image = Image.open(image_path)
    
    # Create configuration
    config = OCRPipelineConfig.create_default()
    
    # Create PDF processor
    processor = PDFProcessor(config)
    
    # Process image
    fragments = processor.process_image(image)
    
    # Print results
    for fragment in fragments:
        print(f"Type: {type(fragment).__name__}")
        print(f"Value: {fragment.value}")
        print(f"Style: {fragment.style}")
        print("---")


def process_image_direct(image_path: str) -> None:
    """Process image directly using OCR pipeline (without PDFProcessor)."""
    
    # Load image
    image = Image.open(image_path)
    
    # Create configuration
    config = OCRPipelineConfig.create_default()
    
    # Create clients
    dots_client = DotsOCRClient(config.dots_ocr_config)
    qwen_client = QwenClient(config.qwen_config)
    
    # Create pipeline components
    detector = DotsBlockDetector(dots_client)
    recognizer = QwenBlockRecognizer(qwen_client)
    
    # Create pipeline
    pipeline = ScanPipeline(
        detector=detector,
        recognizer=recognizer
    )
    
    # Process image
    fragments = pipeline.process(image)
    
    # Print results
    for fragment in fragments:
        print(f"Type: {type(fragment).__name__}")
        print(f"Value: {fragment.value}")
        print(f"Style: {fragment.style}")
        print("---")


if __name__ == "__main__":
    # Example usage
    print("=== Processing image via PDFProcessor ===")
    process_image("example.png")
    
    print("\n=== Processing image directly via OCR pipeline ===")
    process_image_direct("example.png")
    
    # process_pdf("example.pdf", page_image, page_num=0)
