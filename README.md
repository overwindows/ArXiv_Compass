# 🎯 ArXiv Compass

> Your intelligent navigator through the sea of academic papers

ArXiv Compass is a modern, intelligent interface for exploring and managing academic papers from ArXiv. It helps researchers cut through information overload by providing smart search, personalized recommendations, and an intuitive paper management system.

## ✨ Features

- 🔍 **Smart Search**: Find papers using natural language or advanced queries
- 🎯 **Personalized Recommendations**: Get paper suggestions based on your interests
- 📚 **Personal Library**: Save and organize papers that matter to you
- 🔄 **Similar Paper Discovery**: Find related papers based on content similarity
- 📈 **Trending Papers**: See what's gaining attention in your field
- 📅 **Daily Updates**: Stay current with the latest publications

## 🚀 Getting Started

### Prerequisites

You'll need Python 3.7+ and the following system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get install imagemagick poppler-utils

# macOS
brew install imagemagick poppler
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/overwindows/arxiv-compass.git
cd arxiv-compass
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🛠️ Setup Process

1. **Fetch Papers**
   ```bash
   python3 fetch_papers.py --start-date 2025-01-01 --end-date 2025-02-10
   ```

2. **Download PDFs**
   ```bash
   python3 download_pdfs.py
   ```

3. **Process Papers**
   ```bash
   python3 parse_pdf_to_text.py  # Extract text from PDFs
   python3 thumb_pdf.py          # Generate thumbnails
   python3 analyze.py            # Compute paper vectors
   ```

4. **Initialize Database**
   ```bash
   sqlite3 as.db < schema.sql   # First time only
   python3 make_cache.py
   ```

5. **Start Server**
   ```bash
   python3 serve.py
   ```

Visit `http://localhost:5000` to start exploring papers! 🎉

## 🔧 Configuration

- Modify `fetch_papers.py` to customize which ArXiv categories to track
- Adjust constants in `download_pdfs.py` for download behavior
- Configure server settings in `serve.py`

## 🌟 Production Deployment

For production deployment:

1. Create a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(16))" > secret_key.txt
```

2. Run the server with production flags:
```bash
python serve.py --prod --port 80
```

## 🔄 Daily Updates

To keep your instance fresh, run the following daily:

```bash
./update.sh
```

Or set up a cron job:
```bash
0 1 * * * cd /path/to/arxiv-compass && ./update.sh >> update.log 2>&1
```

## 📊 Performance Tips

- Link numpy with BLAS for faster computations
- Use SSD storage for the paper database
- Consider using a CDN for PDF serving
- Enable caching in production

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original arxiv-sanity-preserver by Andrej Karpathy
- ArXiv for providing the paper database
- All contributors to the project

---
