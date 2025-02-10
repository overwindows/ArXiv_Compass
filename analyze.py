"""
Analyze paper content and compute TF-IDF vectors.
This script reads text files of papers, computes TF-IDF vectors, and generates
similarity metrics for paper recommendations.
"""

import os
import pickle
import logging
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Iterator, Tuple
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import spmatrix
from tqdm import tqdm

from utils import Config, safe_pickle_dump

# Constants
MAX_TRAIN = 5000  # Max number of documents for TF-IDF training
MAX_FEATURES = 5000  # Max number of TF-IDF features
MIN_TEXT_LENGTH = 1000  # Minimum document length to consider
MAX_TEXT_LENGTH = 500000  # Maximum document length to consider
BATCH_SIZE = 200  # Batch size for similarity computations
NEAREST_NEIGHBORS = 50  # Number of similar papers to find

@dataclass
class Paper:
    """Class to hold paper data."""
    pid: str  # Paper ID with version
    txt_path: str  # Path to text file
    text_length: int  # Length of paper text

def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_database() -> Dict[str, Any]:
    """Load the papers database."""
    try:
        with open(Config.db_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logging.error(f"Failed to load database: {e}")
        raise

def get_paper_text_path(paper_data: Dict[str, Any]) -> str:
    """Generate text file path for a paper."""
    idvv = f"{paper_data['_rawid']}v{paper_data['_version']}"
    return str(Path(Config.txt_dir) / f"{idvv}.pdf.txt")

def read_paper_text(txt_path: str) -> str:
    """Read and validate paper text content."""
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading {txt_path}: {e}")
        return ""

def collect_valid_papers(db: Dict[str, Any]) -> List[Paper]:
    """Collect papers with valid text content."""
    valid_papers = []
    
    for i, (pid, paper_data) in enumerate(tqdm(db.items(), desc="Reading papers")):
        txt_path = get_paper_text_path(paper_data)
        
        if not os.path.isfile(txt_path):
            logging.warning(f"Text file not found: {txt_path}")
            continue
            
        text = read_paper_text(txt_path)
        text_length = len(text)
        
        if MIN_TEXT_LENGTH <= text_length <= MAX_TEXT_LENGTH:
            valid_papers.append(Paper(
                pid=f"{paper_data['_rawid']}v{paper_data['_version']}", 
                txt_path=txt_path,
                text_length=text_length
            ))
            logging.debug(f"Added paper {pid} with {text_length} chars")
        else:
            logging.warning(f"Skipped paper {pid}: suspicious length {text_length}")
    
    return valid_papers

def make_corpus(papers: List[Paper]) -> Iterator[str]:
    """Create an iterator for paper texts to conserve memory."""
    for paper in papers:
        yield read_paper_text(paper.txt_path)

def train_tfidf(papers: List[Paper]) -> Tuple[TfidfVectorizer, List[Paper]]:
    """Train TF-IDF vectorizer on a subset of papers."""
    # Randomly select training papers
    np.random.seed(1337)
    train_papers = papers.copy()
    np.random.shuffle(train_papers)
    train_papers = train_papers[:min(len(train_papers), MAX_TRAIN)]
    
    logging.info(f"Training TF-IDF on {len(train_papers)} documents...")
    
    vectorizer = TfidfVectorizer(
        input='content',
        encoding='utf-8',
        decode_error='replace',
        strip_accents='unicode',
        lowercase=True,
        analyzer='word',
        stop_words='english',
        token_pattern=r'(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b',
        ngram_range=(1, 2),
        max_features=MAX_FEATURES,
        norm='l2',
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=True,
        max_df=1.0,
        min_df=1
    )
    
    vectorizer.fit(make_corpus(train_papers))
    return vectorizer, train_papers

def compute_similarities(X: np.ndarray, pids: List[str]) -> Dict[str, List[str]]:
    """Compute paper similarities in batches."""
    sim_dict = {}
    total_batches = (len(pids) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for i in tqdm(range(0, len(pids), BATCH_SIZE), desc="Computing similarities", total=total_batches):
        batch_end = min(len(pids), i + BATCH_SIZE)
        xquery = X[i:batch_end]
        
        # Compute similarities
        similarities = -np.asarray(np.dot(X, xquery.T))
        nearest_neighbors = np.argsort(similarities, axis=0)
        
        # Store results
        for j in range(batch_end - i):
            paper_id = pids[i + j]
            similar_papers = [pids[idx] for idx in nearest_neighbors[:NEAREST_NEIGHBORS, j]]
            sim_dict[paper_id] = similar_papers
    
    return sim_dict

def save_results(
    X: spmatrix,
    vectorizer: TfidfVectorizer,
    papers: List[Paper],
    sim_dict: Dict[str, List[str]]
) -> None:
    """Save analysis results to files."""
    # Save TF-IDF matrix
    logging.info(f"Saving TF-IDF matrix to {Config.tfidf_path}")
    safe_pickle_dump({'X': X}, Config.tfidf_path)
    
    # Save metadata
    logging.info(f"Saving metadata to {Config.meta_path}")
    meta_data = {
        'vocab': vectorizer.vocabulary_,
        'idf': vectorizer._tfidf.idf_,
        'pids': [p.pid for p in papers],
        'ptoi': {p.pid: i for i, p in enumerate(papers)}
    }
    safe_pickle_dump(meta_data, Config.meta_path)
    
    # Save similarities
    logging.info(f"Saving similarities to {Config.sim_path}")
    safe_pickle_dump(sim_dict, Config.sim_path)

def main():
    """Main function to coordinate the analysis process."""
    setup_logging()
    
    try:
        # Load and process papers
        db = load_database()
        papers = collect_valid_papers(db)
        logging.info(f"Found {len(papers)} valid papers out of {len(db)} total")
        
        if not papers:
            logging.error("No valid papers found to process")
            return
        
        # Train TF-IDF
        vectorizer, train_papers = train_tfidf(papers)
        
        # Transform all papers
        logging.info(f"Transforming {len(papers)} documents...")
        X = vectorizer.transform(make_corpus(papers))
        logging.info(f"Generated matrix with shape {X.shape}")
        
        # Compute similarities
        X_dense = X.todense()
        sim_dict = compute_similarities(X_dense, [p.pid for p in papers])
        
        # Save results
        save_results(X, vectorizer, papers, sim_dict)
        
        logging.info("Analysis completed successfully!")
        
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    main()
