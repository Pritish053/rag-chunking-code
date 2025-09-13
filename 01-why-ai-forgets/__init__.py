"""
Article 1: Why Your AI Keeps Forgetting Context
Code examples demonstrating chunking problems and quick fixes.
"""

from .naive_chunking_problems import NaiveChunker, ChunkAnalyzer, ChunkProblem
from .quick_fixes import (
    OverlapChunker,
    SentenceAwareChunker,
    ParagraphAwareChunker,
    MetadataPreservingChunker,
    ChunkWithMetadata
)

__all__ = [
    'NaiveChunker',
    'ChunkAnalyzer',
    'ChunkProblem',
    'OverlapChunker',
    'SentenceAwareChunker',
    'ParagraphAwareChunker',
    'MetadataPreservingChunker',
    'ChunkWithMetadata'
]