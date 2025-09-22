"""PDF processor with selectable text support."""

from typing import Iterator, Optional
from PIL import Image
import io

try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

from .pipeline import ScanPipeline
from .detector import DotsBlockDetector
from .recognizer import QwenBlockRecognizer
from .dots_ocr_client import DotsOCRClient
from .qwen_client import QwenClient
from .config import OCRPipelineConfig
from documentor.data.structures.fragment.base import Fragment


class PDFProcessor:
    """PDF processor that handles both selectable text and OCR."""
    
    def __init__(self, config: OCRPipelineConfig):
        self.config = config
        self._setup_ocr_pipeline()
    
    def _setup_ocr_pipeline(self):
        """Setup OCR pipeline components."""
        dots_client = DotsOCRClient(self.config.dots_ocr_config)
        qwen_client = QwenClient(self.config.qwen_config)
        
        detector = DotsBlockDetector(dots_client)
        recognizer = QwenBlockRecognizer(qwen_client)
        
        self.ocr_pipeline = ScanPipeline(
            detector=detector,
            recognizer=recognizer
        )
    
    def extract_selectable_text(self, pdf_path: str, page_num: int = 0) -> Optional[str]:
        """Extract selectable text from PDF page."""
        if not PDF_SUPPORT:
            return None
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if page_num < len(reader.pages):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    return text.strip() if text else None
        except Exception:
            pass
        
        return None
    
    def process_pdf_page(self, pdf_path: str, page_image: Image.Image, page_num: int = 0) -> Iterator[Fragment]:
        """Process PDF page with selectable text support."""
        
        # Try to extract selectable text first
        selectable_text = self.extract_selectable_text(pdf_path, page_num)
        
        if selectable_text and len(selectable_text) > 50:  # Minimum text length
            # Use selectable text - create simple fragments
            yield from self._create_fragments_from_text(selectable_text)
        else:
            # No selectable text - use OCR pipeline
            yield from self.ocr_pipeline.process(page_image)
    
    def _create_fragments_from_text(self, text: str) -> Iterator[Fragment]:
        """Create fragments from selectable text."""
        from documentor.data.structures.fragment import ParagraphFragment
        
        # Split text into paragraphs
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                fragment = ParagraphFragment(
                    value=paragraph,
                    style={
                        'source': 'pdf_selectable_text',
                        'confidence': 1.0
                    }
                )
                yield fragment
    
    def process_image(self, image: Image.Image) -> Iterator[Fragment]:
        """Process image using OCR pipeline."""
        yield from self.ocr_pipeline.process(image)
