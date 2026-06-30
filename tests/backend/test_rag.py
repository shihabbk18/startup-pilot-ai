from uuid import uuid4

from app.services.rag import InMemoryRAGService


def test_rag_returns_citations_for_matching_document() -> None:
    service = InMemoryRAGService()
    project_id = uuid4()
    document_id = uuid4()

    service.index_document(
        project_id=project_id,
        document_id=document_id,
        title="Market Research",
        text="Pet care marketplaces need trust, verified providers, recurring bookings, and insurance.",
    )

    answer = service.answer(project_id=project_id, question="What does pet care need?")

    assert answer.citations
    assert answer.citations[0].document_id == document_id
    assert "Market Research" in answer.answer

