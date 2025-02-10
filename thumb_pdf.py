"""
Generate thumbnail images from PDF files using ImageMagick.
This script creates thumbnail previews for PDF files, handling multi-page PDFs
and providing progress feedback.
"""

import os
import sys
import time
import shutil
import logging
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import Config

# Constants
MAX_WORKERS = 4  # Number of parallel workers
TIMEOUT_SECS = 20  # Timeout for thumbnail generation
MAX_PAGES = 8  # Number of pages to include in thumbnail
THUMB_HEIGHT = 156  # Height of each page thumbnail
MISSING_THUMB = 'static/missing.jpg'  # Path to placeholder image
SLEEP_TIME = 0.01  # Sleep time between processing files

def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def check_dependencies() -> None:
    """
    Check if required external dependencies are installed.
    
    Raises:
        SystemExit: If ImageMagick is not installed
    """
    if not shutil.which('convert'):
        logging.error('ImageMagick is not installed. Please install it first.')
        logging.error('Ubuntu/Debian: sudo apt-get install imagemagick')
        logging.error('macOS: brew install imagemagick')
        sys.exit(1)

def ensure_directories() -> None:
    """Ensure required directories exist."""
    for directory in [Config.thumbs_dir, Config.tmp_dir]:
        Path(directory).mkdir(parents=True, exist_ok=True)

def get_pdf_files() -> List[str]:
    """Get list of PDF files to process."""
    return [f for f in os.listdir(Config.pdf_dir) if f.lower().endswith('.pdf')]

def cleanup_temp_files() -> None:
    """Clean up temporary thumbnail files."""
    for i in range(MAX_PAGES):
        for prefix in ['thumb-', 'thumbbuf-']:
            temp_file = Path(Config.tmp_dir) / f'{prefix}{i}.png'
            if temp_file.exists():
                temp_file.unlink()

def generate_page_thumbnails(pdf_path: str) -> bool:
    """
    Generate individual page thumbnails from PDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cmd = [
            'convert',
            f'{pdf_path}[0-{MAX_PAGES-1}]',
            '-thumbnail',
            f'x{THUMB_HEIGHT}',
            str(Path(Config.tmp_dir) / 'thumb.png')
        ]
        
        process = subprocess.Popen(cmd)
        
        # Wait with timeout
        start_time = time.time()
        while time.time() - start_time < TIMEOUT_SECS:
            if process.poll() is not None:
                return process.returncode == 0
            time.sleep(0.1)
            
        # Kill if still running
        process.terminate()
        process.wait(timeout=1)
        return False
        
    except Exception as e:
        logging.error('Error generating thumbnails: %s', str(e))
        return False

def combine_thumbnails(output_path: str) -> bool:
    """
    Combine individual page thumbnails into final thumbnail.
    
    Args:
        output_path: Path where to save the final thumbnail
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cmd = [
            'montage',
            '-mode', 'concatenate',
            '-quality', '80',
            '-tile', 'x1',
            str(Path(Config.tmp_dir) / 'thumb-*.png'),
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        logging.error('Error combining thumbnails: %s', str(e))
        return False

def create_missing_thumbnail(output_path: str) -> None:
    """Create a placeholder thumbnail for failed conversions."""
    try:
        shutil.copy(MISSING_THUMB, output_path)
    except Exception as e:
        logging.error('Error creating missing thumbnail: %s', str(e))

def process_pdf(args: Tuple[int, int, str]) -> Tuple[int, bool]:
    """
    Process a single PDF file.
    
    Args:
        args: Tuple of (index, total_files, pdf_filename)
        
    Returns:
        Tuple of (index, success_status)
    """
    i, total_files, pdf_file = args
    
    pdf_path = str(Path(Config.pdf_dir) / pdf_file)
    thumb_path = str(Path(Config.thumbs_dir) / f'{pdf_file}.jpg')
    
    # Skip if thumbnail already exists
    if os.path.isfile(thumb_path):
        logging.debug('[%d/%d] Skipping %s, thumbnail exists', 
                     i + 1, total_files, pdf_file)
        return i, True
    
    logging.info('[%d/%d] Processing %s', i + 1, total_files, pdf_file)
    
    cleanup_temp_files()
    
    if not generate_page_thumbnails(pdf_path):
        logging.error('[%d/%d] Failed to generate thumbnails for %s', 
                     i + 1, total_files, pdf_file)
        create_missing_thumbnail(thumb_path)
        return i, False
    
    if not combine_thumbnails(thumb_path):
        logging.error('[%d/%d] Failed to combine thumbnails for %s', 
                     i + 1, total_files, pdf_file)
        create_missing_thumbnail(thumb_path)
        return i, False
    
    return i, True

def main():
    """Main function to coordinate thumbnail generation."""
    setup_logging()
    check_dependencies()
    ensure_directories()
    
    pdf_files = get_pdf_files()
    if not pdf_files:
        logging.warning('No PDF files found in %s', Config.pdf_dir)
        return
    
    logging.info('Found %d PDF files to process', len(pdf_files))
    
    # Statistics
    successful = 0
    failed = 0
    skipped = 0
    
    # Prepare work items
    work_items = [
        (i, len(pdf_files), pdf_file) 
        for i, pdf_file in enumerate(pdf_files)
    ]
    
    # Process files in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_pdf, item) for item in work_items]
        
        for future in as_completed(futures):
            try:
                _, success = future.result()
                if success:
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                logging.error('Error processing file: %s', str(e))
                failed += 1
            
            # Allow for Ctrl+C
            time.sleep(SLEEP_TIME)
    
    # Final statistics
    logging.info('Thumbnail generation completed!')
    logging.info('Successfully processed: %d', successful)
    logging.info('Failed: %d', failed)
    logging.info('Total files processed: %d', len(pdf_files))

if __name__ == "__main__":
    main()
