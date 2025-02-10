"""
Queries arxiv API and downloads papers (the query is a parameter).
The script is intended to enrich an existing database pickle (by default db.p),
so this file will be loaded first, and then new results will be added to it.
"""

import os
import time
import pickle
import random
import argparse
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, Tuple, Optional
import feedparser
from datetime import datetime, timedelta
import urllib.parse

from utils import Config, safe_pickle_dump

# Constants
BASE_URL = 'http://export.arxiv.org/api/query?'
DEFAULT_SEARCH_QUERY = 'cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML'
DEFAULT_START_DATE = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
DEFAULT_END_DATE = datetime.now().strftime('%Y-%m-%d')

def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def encode_feedparser_dict(d: Any) -> Any:
    """
    Helper function to get rid of feedparser bs with a deep copy.
    Converts feedparser's custom dict object into a standard Python dict.
    
    Args:
        d: The feedparser dict or nested structure to convert
        
    Returns:
        A standard Python dict/list/primitive
    """
    if isinstance(d, (feedparser.FeedParserDict, dict)):
        return {k: encode_feedparser_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [encode_feedparser_dict(k) for k in d]
    return d

def parse_arxiv_url(url: str) -> Tuple[str, int]:
    """
    Parse arxiv paper URL to extract paper ID and version.
    
    Args:
        url: The arxiv URL (e.g., http://arxiv.org/abs/1512.08756v2)
    
    Returns:
        Tuple of (paper_id, version)
        
    Raises:
        ValueError: If the URL format is invalid
    """
    try:
        ix = url.rfind('/')
        idversion = url[ix+1:]  # extract just the id (and the version)
        parts = idversion.split('v')
        if len(parts) != 2:
            raise ValueError(f'Invalid URL format: {url}')
        return parts[0], int(parts[1])
    except Exception as e:
        raise ValueError(f'Error parsing URL {url}: {str(e)}')

def build_date_query(start_date: str, end_date: str, search_terms: str) -> str:
    """
    Build arXiv API query with date constraints.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        search_terms: Additional search terms/categories
        
    Returns:
        Formatted query string
    """
    date_query = f'submittedDate:[{start_date}* TO {end_date}*]'
    if search_terms:
        # Combine date and search terms with AND
        query = f'({date_query}) AND ({search_terms})'
    else:
        query = date_query
    return urllib.parse.quote(query)

def fetch_papers(args: argparse.Namespace) -> Dict[str, Any]:
    """
    Fetch papers from arxiv API based on the provided arguments.
    
    Args:
        args: Command line arguments
        
    Returns:
        Dictionary containing the paper database
    """
    logging.info('Searching arXiv from %s to %s', args.start_date, args.end_date)

    # Load existing database
    db: Dict[str, Any] = {}
    try:
        db = pickle.load(open(Config.db_path, 'rb'))
        logging.info('Database has %d entries at start', len(db))
    except Exception as e:
        logging.error('Error loading existing database: %s', e)
        logging.info('Starting from an empty database')

    num_added_total = 0
    start = 0
    
    while True:
        logging.info("Fetching results starting at index %i", start)
        
        query = (f'search_query={build_date_query(args.start_date, args.end_date, args.search_terms)}'
                f'&sortBy=lastUpdatedDate&start={start}&max_results={args.results_per_iteration}')
        
        try:
            with urllib.request.urlopen(BASE_URL + query) as url:
                response = url.read()
        except urllib.error.URLError as e:
            logging.error('Error fetching from arxiv: %s', e)
            break

        parse = feedparser.parse(response)
        num_added = num_skipped = 0

        for entry in parse.entries:
            paper_dict = encode_feedparser_dict(entry)
            
            try:
                rawid, version = parse_arxiv_url(paper_dict['id'])
                paper_dict['_rawid'] = rawid
                paper_dict['_version'] = version

                if rawid not in db or version > db[rawid]['_version']:
                    db[rawid] = paper_dict
                    logging.info('Updated %s added %s', 
                               paper_dict['updated'],
                               paper_dict['title'])
                    num_added += 1
                    num_added_total += 1
                else:
                    num_skipped += 1
            except ValueError as e:
                logging.error('Error processing paper: %s', e)
                continue

        logging.info('Added %d papers, already had %d.', num_added, num_skipped)

        if not parse.entries:
            logging.info('No more results available.')
            break

        if num_added == 0 and args.break_on_no_added == 1:
            logging.info('No new papers were added. Assuming no new papers exist. Exiting.')
            break

        start += args.results_per_iteration
        
        sleep_time = args.wait_time + random.uniform(0, 3)
        logging.info('Sleeping for %.2f seconds', sleep_time)
        time.sleep(sleep_time)

    return db, num_added_total

def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description='Fetch papers from arxiv API')
    parser.add_argument('--start-date', type=str,
                       default=DEFAULT_START_DATE,
                       help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end-date', type=str,
                       default=DEFAULT_END_DATE,
                       help='End date in YYYY-MM-DD format')
    parser.add_argument('--search-terms', type=str,
                       default='cat:cs.CV OR cat:cs.AI OR cat:cs.LG OR cat:cs.CL OR cat:cs.NE OR cat:stat.ML',
                       help='Additional search terms or categories')
    parser.add_argument('--results-per-iteration', type=int, default=100,
                       help='passed to arxiv API')
    parser.add_argument('--wait-time', type=float, default=5.0,
                       help='lets be gentle to arxiv API (in number of seconds)')
    parser.add_argument('--break-on-no-added', type=int, default=1,
                       help='break out early if all returned query papers are already in db? 1=yes, 0=no')
    
    args = parser.parse_args()
    
    # Validate dates
    try:
        datetime.strptime(args.start_date, '%Y-%m-%d')
        datetime.strptime(args.end_date, '%Y-%m-%d')
    except ValueError:
        parser.error('Dates must be in YYYY-MM-DD format')
        
    setup_logging()
    
    db, num_added_total = fetch_papers(args)
    
    # Save the database if we found anything new
    if num_added_total > 0:
        logging.info('Saving database with %d papers to %s', len(db), Config.db_path)
        safe_pickle_dump(db, Config.db_path)

if __name__ == "__main__":
    main()

