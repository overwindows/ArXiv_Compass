"""
Downloads PDF files of papers stored in the database.
Skips papers that have already been downloaded and handles errors gracefully.
"""

import os
import time
import pickle
import shutil
import random
import logging
from pathlib import Path
from urllib.request import urlopen, URLError
from typing import Dict, Any, Tuple

from utils import Config

# Constants
TIMEOUT_SECS = 10  # Timeout for downloading each paper
MAX_RETRIES = 3    # Maximum number of retry attempts per paper
SLEEP_BASE = 0.05  # Base sleep time between downloads
SLEEP_RANDOM = 0.1 # Random additional sleep time

def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def ensure_pdf_dir() -> Path:
    """Ensure PDF directory exists and return its path."""
    pdf_dir = Path(Config.pdf_dir)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    return pdf_dir

def load_database() -> Dict[str, Any]:
    """Load the papers database from pickle file."""
    try:
        with open(Config.db_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logging.error(f"Failed to load database from {Config.db_path}: {e}")
        raise

def download_paper(pdf_url: str, output_path: Path, retry_count: int = 0) -> bool:
    """
    Download a single paper PDF with retry logic.
    
    Args:
        pdf_url: URL of the PDF to download
        output_path: Path where to save the PDF
        retry_count: Current retry attempt number
        
    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        with urlopen(pdf_url, timeout=TIMEOUT_SECS) as response:
            with open(output_path, 'wb') as fp:
                shutil.copyfileobj(response, fp)
        return True
        
    except URLError as e:
        logging.error(f"Network error downloading {pdf_url}: {e}")
    except TimeoutError:
        logging.error(f"Timeout downloading {pdf_url}")
    except Exception as e:
        logging.error(f"Unexpected error downloading {pdf_url}: {e}")
        
    # Retry logic
    if retry_count < MAX_RETRIES:
        time.sleep(SLEEP_BASE * (retry_count + 1))  # Exponential backoff
        return download_paper(pdf_url, output_path, retry_count + 1)
        
    return False

def main():
    """Main function to download PDFs."""
    logging.info("Starting PDF download process")
    
    # Setup
    pdf_dir = ensure_pdf_dir()
    existing_pdfs = set(os.listdir(pdf_dir))
    
    try:
        db = load_database()
    except Exception:
        return
    
    # Download statistics
    total_papers = len(db)
    successful_downloads = 0
    skipped_papers = 0
    failed_downloads = 0
    
    for paper_id, paper_data in db.items():
        try:
            # Find PDF URL
            pdf_links = [x['href'] for x in paper_data['links'] if x['type'] == 'application/pdf']
            if not pdf_links:
                logging.warning(f"No PDF link found for paper {paper_id}")
                failed_downloads += 1
                continue
                
            pdf_url = pdf_links[0] + '.pdf'
            basename = pdf_url.split('/')[-1]
            output_path = pdf_dir / basename
            
            # Skip if already downloaded
            if basename in existing_pdfs:
                logging.debug(f"Skipping {basename} - already downloaded")
                skipped_papers += 1
                successful_downloads += 1
                continue
            
            # Download paper
            logging.info(f"Downloading {basename} from {pdf_url}")
            if download_paper(pdf_url, output_path):
                successful_downloads += 1
                logging.info(f"Successfully downloaded {basename}")
            else:
                failed_downloads += 1
                logging.error(f"Failed to download {basename} after {MAX_RETRIES} attempts")
            
            # Random delay between downloads
            time.sleep(SLEEP_BASE + random.uniform(0, SLEEP_RANDOM))
            
        except Exception as e:
            logging.error(f"Error processing paper {paper_id}: {e}")
            failed_downloads += 1
            continue
        
        # Progress update
        if (successful_downloads + failed_downloads) % 10 == 0:
            logging.info(
                f"Progress: {successful_downloads + failed_downloads}/{total_papers} "
                f"(Success: {successful_downloads}, Failed: {failed_downloads}, "
                f"Skipped: {skipped_papers})"
            )
    
    # Final statistics
    logging.info("Download process completed!")
    logging.info(f"Total papers processed: {total_papers}")
    logging.info(f"Successfully downloaded: {successful_downloads}")
    logging.info(f"Failed downloads: {failed_downloads}")
    logging.info(f"Skipped (already existed): {skipped_papers}")

if __name__ == "__main__":
    setup_logging()
    main()

