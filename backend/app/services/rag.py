from dataclasses import dataclass
from math import log
from uuid import UUID


@dataclass(frozen=True)
class RetrievedCitation:
    document_id: UUID | None
    title: str
    excerpt: str
    score: float


@dataclass(frozen=True)
class RAGAnswer:
    answer: str
    citations: list[RetrievedCitation]


@dataclass(frozen=True)
class IndexedChunk:
    project_id: UUID
    document_id: UUID
    title: str
    content: str
    terms: set[str]


def tokenize(text: str) -> set[str]:
    """Tokenize text into normalized terms for local retrieval."""
    return {
        token.strip(".,:;!?()[]{}\"'").lower()
        for token in text.split()
        if len(token.strip(".,:;!?()[]{}\"'")) > 2
    }


def chunk_text(text: str, max_words: int = 220) -> list[str]:
    """Split text into chunks sized for retrieval."""
    words = text.split()
    if not words:
        return []
    return [" ".join(words[index : index + max_words]) for index in range(0, len(words), max_words)]


class InMemoryRAGService:
    """Local RAG implementation with deterministic lexical retrieval.

    Production deployments should back this interface with OpenAI embeddings and ChromaDB. This
    implementation is complete and useful for tests, local development, and offline demos.
    """

    def __init__(self) -> None:
        self._chunks: list[IndexedChunk] = []

    def index_document(self, project_id: UUID, document_id: UUID, title: str, text: str) -> None:
        chunks = chunk_text(text)
        for chunk in chunks:
            self._chunks.append(
                IndexedChunk(
                    project_id=project_id,
                    document_id=document_id,
                    title=title,
                    content=chunk,
                    terms=tokenize(chunk),
                )
            )

    def search(self, project_id: UUID, query: str, limit: int = 4) -> list[RetrievedCitation]:
        query_terms = tokenize(query)
        if not query_terms:
            return []
        scored: list[RetrievedCitation] = []
        for chunk in self._chunks:
            if chunk.project_id != project_id:
                continue
            overlap = query_terms.intersection(chunk.terms)
            if not overlap:
                continue
            score = len(overlap) * log(len(chunk.terms) + 1)
            scored.append(
                RetrievedCitation(
                    document_id=chunk.document_id,
                    title=chunk.title,
                    excerpt=chunk.content[:500],
                    score=score,
                )
            )
        return sorted(scored, key=lambda item: item.score, reverse=True)[:limit]

    def answer(self, project_id: UUID, question: str) -> RAGAnswer:
        citations = self.search(project_id=project_id, query=question)
        if not citations:
            return RAGAnswer(
                answer="I could not find relevant uploaded document context for that question. Upload or index source documents, then ask again.",
                citations=[],
            )
        citation_text = "\n".join(f"- {item.title}: {item.excerpt}" for item in citations)
        return RAGAnswer(
            answer=(
                "Based on the uploaded project documents, the strongest relevant evidence is:\n"
                f"{citation_text}\n\n"
                "Use this as grounded context for planning decisions; verify critical claims before sharing externally."
            ),
            citations=citations,
        )

