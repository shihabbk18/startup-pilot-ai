# RAG Design

StartupPilot AI uses document-grounded retrieval to answer founder questions from uploaded files.

## Supported Inputs

- PDF
- PowerPoint pitch decks
- Word documents
- Excel files
- Plain text

## Production Flow

1. Validate upload type and tenant authorization.
2. Store original file in Supabase Storage.
3. Extract text with LlamaIndex readers.
4. Chunk text with project and tenant metadata.
5. Generate embeddings with OpenAI or a local embedding model.
6. Store vectors in ChromaDB.
7. Retrieve top chunks for chat and generation context.
8. Include citations in answers and reports.

## Local Flow

The backend includes `InMemoryRAGService`, a deterministic lexical retriever that is complete enough for local tests and offline demos. It is intentionally interface-compatible with a vector-backed implementation.

