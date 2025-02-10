"""
Extract text from PDF files using pdftotext utility.
This script processes PDF files from the pdf directory and creates corresponding
text files in the txt directory. It handles errors gracefully and provides
progress feedback.
"""

import os
import sys
import time
import shutil
import logging
import subprocess
from pathlib import Path
from typing import Set, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import Config

# Constants
MAX_WORKERS = 4  # Number of parallel workers
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
        SystemExit: If pdftotext is not installed
    """
    if not shutil.which('pdftotext'):
        logging.error('pdftotext is not installed. Please install poppler-utils first.')
        logging.error('Ubuntu/Debian: sudo apt-get install poppler-utils')
        logging.error('macOS: brew install poppler')
        sys.exit(1)

def ensure_output_dir(txt_dir: str) -> None:
    """
    Ensure the output directory exists.
    
    Args:
        txt_dir: Path to the text output directory
    """
    txt_path = Path(txt_dir)
    if not txt_path.exists():
        logging.info('Creating directory: %s', txt_dir)
        txt_path.mkdir(parents=True, exist_ok=True)

def get_existing_files(txt_dir: str) -> Set[str]:
    """
    Get set of existing text files.
    
    Args:
        txt_dir: Path to the text output directory
        
    Returns:
        Set of existing text file names
    """
    return set(os.listdir(txt_dir))

def get_pdf_files(pdf_dir: str) -> List[str]:
    """
    Get list of PDF files to process.
    
    Args:
        pdf_dir: Path to the PDF directory
        
    Returns:
        List of PDF file names
    """
    return [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]

def convert_pdf_to_text(
    pdf_path: str,
    txt_path: str,
    timeout: int = 30
) -> Optional[str]:
    """
    Convert a single PDF file to text.
    
    Args:
        pdf_path: Path to the PDF file
        txt_path: Path where to save the text file
        timeout: Maximum time in seconds to wait for conversion
        
    Returns:
        Error message if conversion failed, None if successful
    """
    try:
        # Use subprocess.run instead of os.system for better control and security
        result = subprocess.run(
            ['pdftotext', pdf_path, txt_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode != 0:
            return f"pdftotext failed: {result.stderr}"
            
        # Verify the output file exists and has content
        if not os.path.isfile(txt_path) or os.path.getsize(txt_path) == 0:
            return "Output file is empty or wasn't created"
            
        return None
        
    except subprocess.TimeoutExpired:
        return f"Conversion timed out after {timeout} seconds"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def process_file(args: tuple) -> tuple:
    """
    Process a single PDF file (for use with ThreadPoolExecutor).
    
    Args:
        args: Tuple of (file_index, total_files, pdf_filename)
        
    Returns:
        Tuple of (file_index, success_status, error_message if any)
    """
    i, total_files, pdf_file = args
    
    txt_basename = f"{pdf_file}.txt"
    pdf_path = os.path.join(Config.pdf_dir, pdf_file)
    txt_path = os.path.join(Config.txt_dir, txt_basename)
    
    error = convert_pdf_to_text(pdf_path, txt_path)
    
    if error:
        logging.error('[%d/%d] Failed to convert %s: %s', 
                     i + 1, total_files, pdf_file, error)
        # Create empty file to mark as processed
        Path(txt_path).touch()
        return (i, False, error)
    
    logging.info('[%d/%d] Successfully converted %s', 
                i + 1, total_files, pdf_file)
    return (i, True, None)

def main():
    """Main function to coordinate the PDF to text conversion process."""
    setup_logging()
    check_dependencies()
    ensure_output_dir(Config.txt_dir)
    
    existing_files = get_existing_files(Config.txt_dir)
    pdf_files = get_pdf_files(Config.pdf_dir)
    
    if not pdf_files:
        logging.warning('No PDF files found in %s', Config.pdf_dir)
        return
        
    logging.info('Found %d PDF files to process', len(pdf_files))
    
    # Statistics
    successful = 0
    failed = 0
    skipped = 0
    
    # Prepare work items
    work_items = []
    for i, pdf_file in enumerate(pdf_files):
        txt_basename = f"{pdf_file}.txt"
        if txt_basename in existing_files:
            logging.debug('Skipping %s, already exists', pdf_file)
            skipped += 1
            continue
        work_items.append((i, len(pdf_files), pdf_file))
    
    # Process files in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_file, item) for item in work_items]
        
        for future in as_completed(futures):
            try:
                _, success, _ = future.result()
                if success:
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                logging.error('Error processing file: %s', str(e))
                failed += 1
    
    # Final statistics
    logging.info('Conversion completed!')
    logging.info('Successfully converted: %d', successful)
    logging.info('Failed conversions: %d', failed)
    logging.info('Skipped (already existed): %d', skipped)
    logging.info('Total files processed: %d', len(pdf_files))

if __name__ == "__main__":
    main()

