"""
Quick fixes for chunking problems that you can implement today.
These aren't perfect solutions, but they're much better than naive chunking.
"""

import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ChunkWithMetadata:
    """A chunk with additional context information"""
    content: str
    metadata: Dict[str, Any]
    chunk_index: int
    overlap_with_previous: Optional[str] = None
    overlap_with_next: Optional[str] = None


class OverlapChunker:
    """Chunker with overlap to preserve context at boundaries"""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str) -> List[str]:
        """Create chunks with overlap"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])
            start = end - self.overlap  # Back up for overlap
            
            # Avoid infinite loop on small texts
            if end == len(text):
                break
        
        return chunks


class SentenceAwareChunker:
    """Chunker that respects sentence boundaries"""
    
    def __init__(self, target_size: int = 1000, max_size: int = 1200):
        self.target_size = target_size
        self.max_size = max_size
    
    def chunk(self, text: str) -> List[str]:
        """Split text at sentence boundaries"""
        # Simple sentence splitting (can be improved with NLTK or spaCy)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed max size, start new chunk
            if len(current_chunk) + len(sentence) > self.max_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            # If current chunk hasn't reached target size, keep adding
            elif len(current_chunk) + len(sentence) <= self.target_size:
                current_chunk += " " + sentence if current_chunk else sentence
            # If we're between target and max size, make a decision
            else:
                # Add if it keeps us under max, otherwise start new chunk
                if len(current_chunk) + len(sentence) <= self.max_size:
                    current_chunk += " " + sentence
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks


class ParagraphAwareChunker:
    """Chunker that respects paragraph boundaries"""
    
    def __init__(self, target_size: int = 1000):
        self.target_size = target_size
    
    def chunk(self, text: str) -> List[str]:
        """Split text at paragraph boundaries"""
        # Split by double newlines (paragraphs)
        paragraphs = re.split(r'\n\n+', text)
        
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # If single paragraph is too large, fall back to sentence splitting
            if len(paragraph) > self.target_size:
                sentence_chunker = SentenceAwareChunker(self.target_size)
                para_chunks = sentence_chunker.chunk(paragraph)
                for pc in para_chunks:
                    if len(current_chunk) + len(pc) <= self.target_size:
                        current_chunk += "\n\n" + pc if current_chunk else pc
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = pc
            # Normal case: add whole paragraph
            elif len(current_chunk) + len(paragraph) <= self.target_size:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = paragraph
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks


class MetadataPreservingChunker:
    """Chunker that preserves document structure metadata"""
    
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
        self.section_pattern = re.compile(r'^#+\s+(.+)$', re.MULTILINE)
        self.list_pattern = re.compile(r'^[\s]*[-*•]\s+', re.MULTILINE)
    
    def chunk_with_metadata(self, text: str, doc_title: str = "") -> List[ChunkWithMetadata]:
        """Create chunks with metadata about document structure"""
        chunks_with_metadata = []
        
        # Find all section headers
        sections = []
        for match in self.section_pattern.finditer(text):
            sections.append({
                'title': match.group(1),
                'start': match.start(),
                'level': len(match.group(0).split()[0])  # Count # symbols
            })
        
        # Use sentence-aware chunking as base
        sentence_chunker = SentenceAwareChunker(self.chunk_size)
        chunks = sentence_chunker.chunk(text)
        
        current_position = 0
        current_section = ""
        current_subsection = ""
        
        for i, chunk in enumerate(chunks):
            # Find which section this chunk belongs to
            chunk_start = text.find(chunk, current_position)
            current_position = chunk_start + len(chunk)
            
            # Update section context
            for section in sections:
                if section['start'] <= chunk_start:
                    if section['level'] == 1:
                        current_section = section['title']
                    elif section['level'] == 2:
                        current_subsection = section['title']
            
            # Detect if chunk contains a list
            has_list = bool(self.list_pattern.search(chunk))
            
            # Detect if chunk has code
            has_code = '```' in chunk or 'def ' in chunk or 'function ' in chunk
            
            # Create metadata
            metadata = {
                'doc_title': doc_title,
                'section': current_section,
                'subsection': current_subsection,
                'chunk_index': i,
                'total_chunks': len(chunks),
                'has_list': has_list,
                'has_code': has_code,
                'word_count': len(chunk.split())
            }
            
            # Add overlap information
            overlap_prev = chunks[i-1][-50:] if i > 0 else None
            overlap_next = chunks[i+1][:50] if i < len(chunks) - 1 else None
            
            chunks_with_metadata.append(ChunkWithMetadata(
                content=chunk,
                metadata=metadata,
                chunk_index=i,
                overlap_with_previous=overlap_prev,
                overlap_with_next=overlap_next
            ))
        
        return chunks_with_metadata


def demonstrate_improvements():
    """Show how the quick fixes improve chunking"""
    
    test_document = """
    # Configuration Guide
    
    This guide explains how to configure the system for optimal performance.
    
    ## Database Setup
    
    The database configuration is critical for system performance. You must 
    ensure that connection pooling is properly configured. The recommended 
    pool size is 20 connections for most applications.
    
    Set the following environment variables:
    - DB_HOST: Your database hostname
    - DB_PORT: Database port (default 5432)
    - DB_NAME: Name of your database
    - DB_USER: Database username
    - DB_PASSWORD: Database password
    
    ## Authentication Configuration
    
    Authentication requires setting up OAuth2 with your provider. This 
    involves registering your application and obtaining client credentials.
    
    As mentioned above, the database must be configured first because 
    authentication tokens are stored in the database. Without proper database 
    configuration, authentication will fail silently.
    
    ## Performance Tuning
    
    For optimal performance, adjust the following parameters based on your 
    expected load. These settings directly impact response times and throughput.
    """
    
    print("=" * 60)
    print("COMPARING CHUNKING STRATEGIES")
    print("=" * 60)
    
    # 1. Overlap Strategy
    print("\n1. OVERLAP STRATEGY")
    print("-" * 40)
    overlap_chunker = OverlapChunker(chunk_size=200, overlap=30)
    overlap_chunks = overlap_chunker.chunk(test_document)
    print(f"Created {len(overlap_chunks)} chunks with overlap")
    print("Overlap preserves context at boundaries:")
    for i in range(min(2, len(overlap_chunks))):
        print(f"\n  End of chunk {i}: ...{overlap_chunks[i][-30:]}")
        if i + 1 < len(overlap_chunks):
            print(f"  Start of chunk {i+1}: {overlap_chunks[i+1][:30]}...")
    
    # 2. Sentence-Aware Strategy
    print("\n\n2. SENTENCE-AWARE STRATEGY")
    print("-" * 40)
    sentence_chunker = SentenceAwareChunker(target_size=250)
    sentence_chunks = sentence_chunker.chunk(test_document)
    print(f"Created {len(sentence_chunks)} chunks respecting sentences")
    print("No sentences are cut mid-thought:")
    for i, chunk in enumerate(sentence_chunks[:2]):
        print(f"\n  Chunk {i}:")
        print(f"    Starts with: {chunk[:50]}...")
        print(f"    Ends with: ...{chunk[-50:]}")
    
    # 3. Paragraph-Aware Strategy
    print("\n\n3. PARAGRAPH-AWARE STRATEGY")
    print("-" * 40)
    paragraph_chunker = ParagraphAwareChunker(target_size=300)
    paragraph_chunks = paragraph_chunker.chunk(test_document)
    print(f"Created {len(paragraph_chunks)} chunks respecting paragraphs")
    print("Paragraphs stay together when possible:")
    for i, chunk in enumerate(paragraph_chunks[:2]):
        print(f"\n  Chunk {i}: {len(chunk)} characters")
        print(f"    Preview: {chunk[:80]}...")
    
    # 4. Metadata-Preserving Strategy
    print("\n\n4. METADATA-PRESERVING STRATEGY")
    print("-" * 40)
    metadata_chunker = MetadataPreservingChunker(chunk_size=250)
    metadata_chunks = metadata_chunker.chunk_with_metadata(
        test_document, 
        doc_title="System Configuration Guide"
    )
    print(f"Created {len(metadata_chunks)} chunks with metadata")
    print("Each chunk knows its context:")
    for chunk in metadata_chunks[:3]:
        print(f"\n  Chunk {chunk.chunk_index}:")
        print(f"    Section: {chunk.metadata['section']}")
        print(f"    Has list: {chunk.metadata['has_list']}")
        print(f"    Word count: {chunk.metadata['word_count']}")
        print(f"    Content preview: {chunk.content[:60]}...")


def show_retrieval_improvement():
    """Demonstrate how better chunking improves retrieval"""
    
    print("\n" + "=" * 60)
    print("RETRIEVAL QUALITY IMPROVEMENT")
    print("=" * 60)
    
    document = """
    Error Code Reference
    
    Error 401: Authentication failed. This usually means your API key is 
    invalid or expired. To resolve this, generate a new API key from your 
    dashboard and update your configuration.
    
    Error 403: Permission denied. Your API key doesn't have permission for 
    this operation. Contact your administrator to update your access level.
    
    Error 429: Rate limit exceeded. You've made too many requests. Wait a 
    few minutes before trying again, or upgrade your plan for higher limits.
    """
    
    # Simulate a search for "rate limit error"
    search_query = "rate limit error"
    
    print(f"\nSearch query: '{search_query}'")
    print("\nWith naive chunking (might split error codes from descriptions):")
    naive_chunker = NaiveChunker(chunk_size=150)
    naive_chunks = naive_chunker.chunk(document)
    for i, chunk in enumerate(naive_chunks):
        if "429" in chunk or "rate limit" in chunk.lower():
            print(f"  Retrieved chunk {i}: {chunk[:100]}...")
    
    print("\nWith sentence-aware chunking (keeps error codes with descriptions):")
    better_chunker = SentenceAwareChunker(target_size=150)
    better_chunks = better_chunker.chunk(document)
    for i, chunk in enumerate(better_chunks):
        if "429" in chunk or "rate limit" in chunk.lower():
            print(f"  Retrieved chunk {i}: {chunk[:150]}...")


if __name__ == "__main__":
    demonstrate_improvements()
    show_retrieval_improvement()