## RAG With Open Search

📚 Parse documents using Docling's document conversion capabilities \
🧩 Perform hierarchical chunking of the documents using Docling \
🔢 Generate text embeddings on document chunks \
🤖 Perform RAG using OpenSearch and the LlamaIndex framework \
🛠️ Leverage the transformation and structure capabilities of Docling documents for RAG

**Tools**
- OpenSearch, an open-source search and analytics tool.
- LlamaIndex framework to perform RAG over documents parsed by Docling.

**Creating Virtual Env**

```
python3 -m venv rag_opensearch
source rag_opensearch/bin/activate
pip install notebook ipywidgets docling llama-index-readers-file llama-index-readers-docling llama-index-readers-elasticsearch llama-index-node-parser-docling llama-index-vector-stores-opensearch llama-index-embeddings-huggingface llama-index-llms-ollama
```

**Key Takeways**

- How to improve RAG performance with Docling filtering techniques.
- How to utilize RRF with Hybrid Search for better Retrieval.
