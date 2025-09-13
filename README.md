# RAG Chunking Strategies: Code Examples

Complete code examples for the Medium article series on RAG chunking strategies. Each article has its own folder with working implementations, benchmarks, and practical examples.

## 📚 Article Series

1. **[Why Your AI Keeps Forgetting Context](./01-why-ai-forgets/)** - Understanding the chunking problem
2. **[Chunking Fundamentals](./02-chunking-fundamentals/)** - Basic strategies and implementations
3. **[Hierarchy-Based Chunking](./03-hierarchy-based/)** - Respecting document structure
4. **[Semantic & Recursive Chunking](./04-semantic-recursive/)** - Advanced meaning-aware strategies
5. **[Chunking Face-off](./05-chunking-faceoff/)** - Performance comparisons and benchmarks
6. **[File Format Challenges](./06-file-formats/)** - PDFs, tables, images, and more
7. **[Production Pipelines](./07-production-pipelines/)** - Building robust systems

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Pritish053/rag-chunking-code.git
cd rag-chunking-code

# Install dependencies
pip install -r requirements.txt

# Run the examples for article 1
python 01-why-ai-forgets/naive_chunking_problems.py
```

## 📁 Repository Structure

```
.
├── 01-why-ai-forgets/          # Code for article 1
│   ├── naive_chunking_problems.py
│   ├── quick_fixes.py
│   └── examples/
├── 02-chunking-fundamentals/   # Code for article 2
│   ├── fixed_size_chunking.py
│   ├── sentence_based_chunking.py
│   └── paragraph_chunking.py
├── 03-hierarchy-based/         # Code for article 3
│   ├── markdown_chunker.py
│   ├── html_chunker.py
│   └── document_structure.py
├── 04-semantic-recursive/      # Code for article 4
│   ├── semantic_chunker.py
│   ├── recursive_splitter.py
│   └── embedding_analysis.py
├── 05-chunking-faceoff/        # Code for article 5
│   ├── benchmark_suite.py
│   ├── evaluation_metrics.py
│   └── results/
├── 06-file-formats/            # Code for article 6
│   ├── pdf_chunker.py
│   ├── table_processor.py
│   └── multimodal_chunking.py
├── 07-production-pipelines/    # Code for article 7
│   ├── pipeline.py
│   ├── monitoring.py
│   └── deployment/
├── utils/                      # Shared utilities
│   ├── tokenizer.py
│   ├── embeddings.py
│   └── evaluation.py
├── examples/                   # Sample documents and data
│   ├── documents/
│   └── test_data/
└── tests/                      # Unit tests
    └── test_*.py
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip or conda

### Install Dependencies

```bash
pip install -r requirements.txt
```

For development:
```bash
pip install -r requirements-dev.txt
```

## 💡 Usage Examples

### Basic Naive Chunking (Article 1)

```python
from chunking_strategies import NaiveChunker

# This is what NOT to do
chunker = NaiveChunker(chunk_size=1000)
chunks = chunker.chunk(document_text)

# See the problems it creates
from chunking_strategies import analyze_chunks
problems = analyze_chunks(chunks)
print(f"Found {len(problems)} issues with naive chunking")
```

### Better Chunking with Overlap (Article 1 Quick Fix)

```python
from chunking_strategies import OverlapChunker

# A quick improvement
chunker = OverlapChunker(chunk_size=1000, overlap=100)
chunks = chunker.chunk(document_text)
```

### Sentence-Aware Chunking (Article 2)

```python
from chunking_strategies import SentenceChunker

# Respects sentence boundaries
chunker = SentenceChunker(target_size=1000)
chunks = chunker.chunk(document_text)
```

## 📊 Benchmarks

Run the benchmark suite to compare different strategies:

```bash
python 05-chunking-faceoff/benchmark_suite.py --input examples/documents/technical_manual.pdf
```

## 🧪 Testing

Run all tests:
```bash
pytest tests/
```

Run specific test suite:
```bash
pytest tests/test_semantic_chunking.py -v
```

## 📈 Performance Metrics

Each chunking strategy is evaluated on:
- **Semantic Coherence**: How well meaning is preserved
- **Retrieval Accuracy**: How often the right chunks are found
- **Processing Speed**: Time to chunk documents
- **Memory Usage**: RAM requirements
- **Token Efficiency**: Optimal use of model context

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Examples inspired by real-world RAG implementations at Xcelcode
- Built with LangChain, OpenAI, and other excellent tools
- Special thanks to the open-source community

## 📬 Contact

- **Author**: Pritish Maheta
- **Medium**: [Follow the series](https://medium.com/@pritishmaheta)
- **LinkedIn**: [Connect with me](https://linkedin.com/in/pritishmaheta)

## ⭐ Star History

If you find this helpful, please star the repository!

---

*Part of the "Mastering RAG Chunking Strategies" series on Medium*