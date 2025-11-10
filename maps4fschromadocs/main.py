"""
Simplified maps4fs documentation ingestion for ChromaDB
GPU-optimized for high-quality embeddings - always rebuilds from scratch

Original plan:
- shallow clone github.com/iwatkot/maps4fs
- find the docs folder
- use all md files from there (excluding SUMMARY.md)
- save it to a chroma_db

GPU Optimizations for ingestion:
- Uses high-quality embedding model (nomic-embed-text or similar)
- Smaller chunk sizes (800) for better retrieval precision
- Higher overlap (300) for better context preservation
- Multi-threaded processing where possible
- Always rebuilds database (no incremental mode complexity)
- Only processes .md files (no docx conversion overhead)

Note: Final model inference will be on CPU, but this preprocessing is on GPU
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# ============================================================================
# CONFIGURATION - GPU Optimized for High-Quality Embeddings
# ============================================================================

# Repository settings
REPO_URL = "https://github.com/iwatkot/maps4fs.git"
DOCS_SUBDIR = "docs"

# Database directory
CHROMA_DB_DIR = "chroma_db"

# GPU-optimized chunking settings for better retrieval quality
CHUNK_SIZE = 800  # Smaller chunks for more precise retrieval
CHUNK_OVERLAP = 300  # Higher overlap for better context preservation

# High-quality embedding model for GPU processing
# Options: "nomic-embed-text", "mxbai-embed-large", or "snowflake-arctic-embed:l"
EMBEDDING_MODEL = "nomic-embed-text"  # High-quality, GPU-optimized model


def clone_repository():
    """Clone the maps4fs repository to a temporary directory"""
    print("Cloning maps4fs repository...")

    # Use temporary directory
    temp_dir = tempfile.mkdtemp(prefix="maps4fs_")

    try:
        # Shallow clone for speed
        subprocess.run(
            ["git", "clone", "--depth", "1", REPO_URL, temp_dir],
            check=True,
            capture_output=True,
            text=True,
        )

        print(f"✓ Repository cloned to: {temp_dir}")
        return temp_dir

    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to clone repository: {e}")
        print(f"Error output: {e.stderr}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return None


def load_markdown_documents(docs_dir):
    """Load markdown files from docs directory, excluding SUMMARY.md"""
    print(f"Loading markdown files from {docs_dir}...")

    documents = []
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        print(f"✗ Docs directory not found: {docs_dir}")
        return documents

    # Find all .md files, excluding SUMMARY.md
    md_files = [f for f in docs_path.rglob("*.md") if f.name.lower() != "summary.md"]

    print(f"Found {len(md_files)} markdown files (excluding SUMMARY.md)")

    for md_file in md_files:
        try:
            # Load with TextLoader for proper encoding handling
            loader = TextLoader(str(md_file), encoding="utf-8")
            doc = loader.load()[0]  # TextLoader returns a list with one document

            # Add relative path to metadata for better context
            relative_path = md_file.relative_to(docs_path)
            doc.metadata["source"] = str(relative_path)
            doc.metadata["full_path"] = str(md_file)

            documents.append(doc)
            print(f"  ✓ Loaded: {relative_path}")

        except Exception as e:
            print(f"  ⚠ Warning: Failed to load {md_file}: {e}")

    print(f"✓ Successfully loaded {len(documents)} markdown documents")
    return documents


def create_vector_database(documents):
    """Create ChromaDB vector database from documents"""
    print("Creating vector database...")

    if not documents:
        print("✗ No documents to process")
        return False

    # Split documents into chunks
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    # Remove existing database
    if os.path.exists(CHROMA_DB_DIR):
        print(f"Removing existing database: {CHROMA_DB_DIR}")
        shutil.rmtree(CHROMA_DB_DIR)

    # Create embeddings (high-quality GPU model)
    print(f"Creating embeddings using {EMBEDDING_MODEL}...")
    print("🚀 Using GPU for fast, high-quality embedding generation...")

    try:
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

        # Create new vector database
        Chroma.from_documents(
            documents=chunks, embedding=embeddings, persist_directory=CHROMA_DB_DIR
        )

        print("✓ Vector database created successfully!")
        print(f"  Location: {CHROMA_DB_DIR}")
        print(f"  Documents processed: {len(documents)}")
        print(f"  Total chunks: {len(chunks)}")

        return True

    except Exception as e:
        print(f"✗ Failed to create vector database: {e}")
        return False


def main():
    """Main function to orchestrate the ingestion process"""
    print("=" * 80)
    print("MAPS4FS DOCUMENTATION INGESTION")
    print("GPU-Optimized for High-Quality Embeddings")
    print("=" * 80)

    temp_dir = None

    try:
        # Step 1: Clone repository
        temp_dir = clone_repository()
        if not temp_dir:
            return

        # Step 2: Locate docs directory
        docs_dir = os.path.join(temp_dir, DOCS_SUBDIR)

        # Step 3: Load markdown documents
        documents = load_markdown_documents(docs_dir)

        # Step 4: Create vector database
        success = create_vector_database(documents)

        if success:
            print("\n" + "=" * 80)
            print("✓ INGESTION COMPLETED SUCCESSFULLY!")
            print(f"Your ChromaDB is ready at: {CHROMA_DB_DIR}")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("✗ INGESTION FAILED")
            print("=" * 80)

    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                print(f"\nCleaning up temporary directory: {temp_dir}")
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"⚠ Warning: Failed to remove temporary directory: {e}")


if __name__ == "__main__":
    main()
