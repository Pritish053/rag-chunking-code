"""
Demonstrating the problems with naive chunking strategies.
This code shows what NOT to do and why it causes issues.
"""

import textwrap
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ChunkProblem:
    """Represents a problem found in chunked text"""
    chunk_index: int
    problem_type: str
    description: str
    example: str


class NaiveChunker:
    """The problematic naive approach to chunking"""
    
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
    
    def chunk(self, text: str) -> List[str]:
        """
        Naive chunking: just split at fixed character intervals.
        This is what causes all the problems!
        """
        return [text[i:i+self.chunk_size] 
                for i in range(0, len(text), self.chunk_size)]


class ChunkAnalyzer:
    """Analyze chunks to find problems"""
    
    def __init__(self):
        self.sentence_endings = ['.', '!', '?']
        self.reference_phrases = [
            'as mentioned above',
            'see table',
            'following the previous',
            'as described earlier',
            'refer to section'
        ]
    
    def analyze_chunks(self, chunks: List[str]) -> List[ChunkProblem]:
        """Find all the problems in a set of chunks"""
        problems = []
        
        for i, chunk in enumerate(chunks):
            # Check for mid-sentence breaks
            if i > 0 and not chunks[i-1].rstrip().endswith(tuple(self.sentence_endings)):
                problems.append(ChunkProblem(
                    chunk_index=i,
                    problem_type="Semantic Break",
                    description="Chunk starts mid-sentence",
                    example=chunk[:50] + "..."
                ))
            
            # Check for broken references
            for phrase in self.reference_phrases:
                if phrase in chunk.lower():
                    problems.append(ChunkProblem(
                        chunk_index=i,
                        problem_type="Reference Loss",
                        description=f"Contains reference '{phrase}' but context may be in different chunk",
                        example=self._extract_context(chunk, phrase)
                    ))
            
            # Check for isolated list items
            if chunk.strip().startswith(('- ', '* ', '• ', '1. ', '2. ', '3. ')):
                if i == 0 or not chunks[i-1].rstrip().endswith(':'):
                    problems.append(ChunkProblem(
                        chunk_index=i,
                        problem_type="Structural Destruction",
                        description="List item separated from header",
                        example=chunk[:50] + "..."
                    ))
        
        return problems
    
    def _extract_context(self, text: str, phrase: str, context_size: int = 30) -> str:
        """Extract context around a phrase"""
        idx = text.lower().find(phrase)
        if idx == -1:
            return ""
        start = max(0, idx - context_size)
        end = min(len(text), idx + len(phrase) + context_size)
        return "..." + text[start:end] + "..."


def demonstrate_problems():
    """Show real examples of chunking problems"""
    
    # Example 1: Medical document
    medical_text = """
    MEDICATION GUIDELINES
    
    For standard adult patients, the recommended dosage is 50mg twice daily, 
    taken with food to minimize gastric irritation. The medication should be 
    stored at room temperature and protected from light.
    
    However, patients with severe kidney disease should not take this medication. 
    Instead, alternative treatment options include lifestyle modifications and 
    dietary changes as discussed with your healthcare provider.
    
    Common side effects include nausea, headache, and dizziness. If you experience 
    any severe reactions, discontinue use immediately and contact your doctor.
    """
    
    # Example 2: Technical documentation
    technical_text = """
    API ENDPOINT: /api/v2/users/create
    
    This endpoint creates a new user in the system. Authentication is required 
    using Bearer token in the Authorization header.
    
    Required Parameters:
    - username: string (3-20 characters)
    - email: valid email address
    - password: string (minimum 8 characters)
    
    Optional Parameters:
    - firstName: string
    - lastName: string
    - phoneNumber: string (E.164 format)
    
    The response will include the created user object with a unique ID. 
    As mentioned above, authentication is required for this endpoint.
    
    Error Codes:
    - 400: Invalid parameters
    - 401: Authentication failed
    - 409: Username or email already exists
    """
    
    # Example 3: Legal document
    legal_text = """
    LIABILITY CLAUSE
    
    The Company shall exercise reasonable care in the performance of its services. 
    However, except in cases of gross negligence or willful misconduct, the Company 
    shall not be held liable for any indirect, incidental, special, or consequential 
    damages arising out of or in connection with the services provided.
    
    The total liability of the Company, regardless of the cause of action, shall not 
    exceed the total amount paid by the Client for the specific services giving rise 
    to the claim.
    """
    
    print("=" * 60)
    print("DEMONSTRATING NAIVE CHUNKING PROBLEMS")
    print("=" * 60)
    
    examples = [
        ("Medical Document", medical_text),
        ("Technical Documentation", technical_text),
        ("Legal Document", legal_text)
    ]
    
    chunker = NaiveChunker(chunk_size=200)  # Deliberately small to show problems
    analyzer = ChunkAnalyzer()
    
    for title, text in examples:
        print(f"\n{title}:")
        print("-" * 40)
        
        chunks = chunker.chunk(text)
        problems = analyzer.analyze_chunks(chunks)
        
        print(f"Created {len(chunks)} chunks")
        print(f"Found {len(problems)} problems:")
        
        for problem in problems[:3]:  # Show first 3 problems
            print(f"\n  • {problem.problem_type} in chunk {problem.chunk_index}")
            print(f"    {problem.description}")
            if problem.example:
                print(f"    Example: {problem.example}")
        
        # Show a particularly bad chunk split
        print("\n  Worst chunk split example:")
        for i, chunk in enumerate(chunks):
            if "should not" in chunk or "shall not" in chunk:
                print(f"    Chunk {i}: ...{chunk.strip()[:100]}...")
                if i + 1 < len(chunks):
                    print(f"    Chunk {i+1}: ...{chunks[i+1].strip()[:100]}...")
                break


def show_context_loss():
    """Demonstrate how context gets lost between chunks"""
    
    document = """
    The configuration process consists of three main steps that must be 
    completed in order. First, initialize the database connection using 
    the provided credentials. Second, set up the authentication middleware 
    with your API keys. Third, configure the rate limiting parameters.
    
    It is critical that you complete these steps before proceeding. 
    Failure to properly initialize the system will result in runtime errors 
    that can be difficult to diagnose.
    
    As mentioned above, the three steps must be completed in order. Each 
    step depends on the successful completion of the previous step. The 
    system will not function correctly if any step is skipped or performed 
    out of sequence.
    """
    
    print("\n" + "=" * 60)
    print("CONTEXT LOSS DEMONSTRATION")
    print("=" * 60)
    
    chunker = NaiveChunker(chunk_size=150)
    chunks = chunker.chunk(document)
    
    print(f"\nOriginal text has clear context about 'three steps'")
    print(f"After chunking into {len(chunks)} pieces:\n")
    
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}:")
        print(textwrap.fill(chunk.strip(), width=60, initial_indent="  ", 
                           subsequent_indent="  "))
        print()
    
    print("Notice how:")
    print("  • 'It' in chunk 1 has lost its reference")
    print("  • 'As mentioned above' in chunk 2 references content not in that chunk")
    print("  • The critical relationship between the steps is broken")


if __name__ == "__main__":
    demonstrate_problems()
    show_context_loss()