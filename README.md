# Maps4FS Documentation ChromaDB Ingestion

GPU-optimized script to ingest maps4fs documentation into ChromaDB with high-quality embeddings. While ingestion uses GPU for speed and quality, the resulting database works with any model (including CPU-only setups).

## Prerequisites

1. **Python 3.8+** installed
2. **Git** installed and accessible from command line
3. **Ollama** installed with GPU support
4. **GPU** with sufficient VRAM for embedding model

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama (if not already installed):
   - Visit [ollama.ai](https://ollama.ai) for installation instructions

3. Pull a high-quality embedding model (choose one):
```bash
# Recommended - balanced quality/speed
ollama pull nomic-embed-text

# Alternative high-quality options:
ollama pull mxbai-embed-large
ollama pull snowflake-arctic-embed:l
```

## Usage

Simply run the main script:

```bash
cd maps4fschromadocs
python main.py
```

The script will:
1. Clone the maps4fs repository (shallow clone)
2. Find and load all `.md` files from the `docs` folder (excluding `SUMMARY.md`)
3. Split documents into optimized chunks (800 chars with 300 overlap for precision)
4. Create high-quality embeddings using GPU acceleration
5. Store everything in a `chroma_db` folder
6. Clean up temporary files

## GPU Optimizations

- **High-quality model**: Uses `nomic-embed-text` or similar for better embeddings
- **Smaller chunks**: 800 characters for more precise retrieval
- **Higher overlap**: 300 characters for better context preservation  
- **GPU acceleration**: Fast embedding generation with GPU support
- **Always rebuilds**: No incremental mode complexity
- **Markdown only**: Skips docx conversion overhead

## Output

- ChromaDB will be created in the `chroma_db` folder
- Database works with any model (CPU or GPU) for inference
- High-quality embeddings provide better retrieval performance
- All temporary files are automatically cleaned up

## Troubleshooting

- **Git not found**: Make sure Git is installed and in your PATH
- **Ollama model not found**: Run `ollama pull nomic-embed-text`
- **GPU memory issues**: Try a smaller embedding model or ensure sufficient VRAM
- **Network issues**: Script needs internet access to clone the repository