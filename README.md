<div align="center" markdown>

[![Maps4FS](https://img.shields.io/badge/maps4fs-gray?style=for-the-badge)](https://github.com/iwatkot/maps4fs)
[![PYDTMDL](https://img.shields.io/badge/pydtmdl-blue?style=for-the-badge)](https://github.com/iwatkot/pydtmdl)
[![PYGDMDL](https://img.shields.io/badge/pygmdl-teal?style=for-the-badge)](https://github.com/iwatkot/pygmdl)  
[![Maps4FS API](https://img.shields.io/badge/maps4fs-api-green?style=for-the-badge)](https://github.com/iwatkot/maps4fsapi)
[![Maps4FS UI](https://img.shields.io/badge/maps4fs-ui-blue?style=for-the-badge)](https://github.com/iwatkot/maps4fsui)
[![Maps4FS Data](https://img.shields.io/badge/maps4fs-data-orange?style=for-the-badge)](https://github.com/iwatkot/maps4fsdata)
[![Maps4FS ChromaDocs](https://img.shields.io/badge/maps4fs-chromadocs-orange?style=for-the-badge)](https://github.com/iwatkot/maps4fschromadocs)  
[![Maps4FS Upgrader](https://img.shields.io/badge/maps4fs-upgrader-yellow?style=for-the-badge)](https://github.com/iwatkot/maps4fsupgrader)
[![Maps4FS Stats](https://img.shields.io/badge/maps4fs-stats-red?style=for-the-badge)](https://github.com/iwatkot/maps4fsstats)
[![Maps4FS Bot](https://img.shields.io/badge/maps4fs-bot-teal?style=for-the-badge)](https://github.com/iwatkot/maps4fsbot)

</div>

<div align="center">
    
<img src="https://github.com/iwatkot/maps4fschromadocs/releases/download/0.0.1/chromadocs-1280-640.png">

<p align="center">
    <a href="#maps4fs-documentation-chromadb-ingestion">Overview</a> •
    <a href="#prerequisites">Prerequisites</a> •
    <a href="#setup">Setup</a> •
    <a href="#usage">Usage</a><br>
    <a href="#gpu-optimizations">GPU Optimizations</a> •
    <a href="#output">Output</a> •
    <a href="#troubleshooting">Troubleshooting</a>
</p>

</div>

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
2. Find and load all `.md` files from the `docs` folder
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
