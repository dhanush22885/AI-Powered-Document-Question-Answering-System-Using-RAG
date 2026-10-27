RAG-Based Intelligent Document Question Answering System

An AI-powered document assistant that allows users to upload PDF documents and ask natural-language questions. The system uses Retrieval-Augmented Generation (RAG), vector embeddings, semantic search, and a Large Language Model (LLM) to generate answers grounded in the content of uploaded documents.

The application is designed for general-purpose document question answering, including medical documents, chemistry textbooks, research papers, educational materials, technical manuals, and other text-based PDFs.

Key Features

PDF Upload: Upload PDF documents through the application interface.
Document Processing: Extract text from PDFs and split it into smaller, manageable chunks.
Semantic Embeddings: Convert document chunks and user questions into numerical vector representations.
Vector Storage: Store document embeddings and associated metadata in Pinecone.
Semantic Retrieval: Retrieve document chunks that are semantically relevant to the user's question.
LLM-Based Answers: Generate natural-language responses using the configured language model.
Context-Aware Question Answering: Provide the retrieved document content as context for answer generation.
Multi-Domain Support: Process documents from different subjects without requiring a separate model for every subject.
Interactive Interface: Allow users to upload documents and ask questions through the application UI.

Technology Stack
Component
Technology

Purpose

Large Language Model
openai/gpt-oss-120b
Generates answers from retrieved context

Embeddings
Google Generative AI or BGE
Converts text into numerical vectors

Vector Database
Pinecone
Stores embeddings and retrieves relevant chunks

AI Framework
LangChain
Connects document loaders, splitters, embeddings, retrievers, and LLMs

Backend
FastAPI
Exposes document-upload and question-answering APIs

PDF Processing
PyPDFLoader
Extracts text and page metadata from PDF files

Text Chunking
RecursiveCharacterTextSplitter
Splits extracted text into smaller overlapping chunks

Frontend
Streamlit, HTML, CSS

Provides the user interface, depending on the implemented frontend

Configuration

python-dotenv

Loads API keys and environment variables

Progress Reporting

tqdm

Displays progress during document processing and vector uploads

API Server

Uvicorn

Runs the FastAPI application

Programming Language

Python

Implements the backend and RAG pipeline

Configuration note: Choose the embedding model you actually use. Google Generative AI embeddings and BGE are alternatives, not necessarily simultaneous components. The vector dimension configured in Pinecone must match the selected embedding model's output dimension.

The openai/gpt-oss-120b model is an open-weight model, not a model served through the OpenAI API. Specify the actual inference provider or runtime used by the application, such as a compatible hosted inference service or a supported self-hosted deployment.

System Architecture

The application follows a Retrieval-Augmented Generation (RAG) architecture. It has two main workflows:
Document ingestion: Processes PDFs and stores their embeddings.
Question answering: Retrieves relevant document chunks and uses them to generate an answer.

Architecture Diagram

flowchart TD
    A[User] --> B[Frontend: Streamlit or HTML/CSS]
    B --> C[FastAPI Backend]
    C --> D[PDF Upload and Validation]
    D --> E[PDF Text Extraction]
    E --> F[Text Chunking]
    F --> G[Embedding Model]
    G --> H[Pinecone Vector Database]

    B --> I[User Question]
    I --> C
    C --> J[Question Embedding]
    J --> K[Semantic Search]
    H --> K
    K --> L[Relevant Document Chunks]
    L --> M[Prompt Construction]
    M --> N[Large Language Model]
    N --> O[Generated Answer]
    O --> B

End-to-End Workflow

Phase 1: Document Ingestion

Step 1 — Upload a document
The user uploads a PDF using the frontend. The file is sent to the FastAPI backend through an upload endpoint.
The backend validates the uploaded file and prepares it for processing.

Step 2 — Extract text from the PDF
PyPDFLoader extracts text from the document and creates document objects containing page content and metadata.
Metadata can include information such as the source filename and page number.

Step 3 — Split the document into chunks
RecursiveCharacterTextSplitter divides the extracted text into smaller chunks.
For example, a textbook containing many pages can be divided into smaller sections that are easier to embed and retrieve.
Chunk size and overlap should be selected according to the document structure and retrieval requirements.

Step 4 — Generate embeddings
The selected embedding model converts each text chunk into a numerical vector representing its semantic meaning.
Similar concepts can have nearby vector representations, allowing retrieval based on meaning rather than exact keyword matching.

Step 5 — Store vectors in Pinecone
The system stores the generated vectors alongside their text content or retrievable document metadata.
Each record should have a unique identifier. Useful metadata includes the source filename, page number, and document identifier.
The stored vectors form the searchable knowledge base for subsequent questions.

Phase 2: Question Answering

Step 6 — Receive the user's question
The user submits a question through the interface.

For example:
Medical document: "What symptoms are listed in the report?"
Chemistry textbook: "Explain the difference between ionic and covalent bonds."
English document: "What is the main idea of this passage?"
Programming guide: "How does a Python dictionary work?"

Step 7 — Convert the question into an embedding
The same embedding model used for the document chunks converts the user's question into a vector.
Using the same compatible embedding space is essential for meaningful similarity search.

Step 8 — Retrieve relevant chunks
The backend searches Pinecone for document vectors that are most similar to the question vector.
The retriever selects the most relevant chunks and their associated metadata. This step is called semantic retrieval.
If multiple documents are uploaded, document IDs or metadata filters can help restrict retrieval to the intended document collection.

Step 9 — Construct the prompt
The backend combines the user's question with the retrieved text chunks and instructions for the LLM.
The prompt should instruct the model to prioritize the supplied context and acknowledge when the available documents do not contain enough information.

Step 10 — Generate the answer
The configured LLM receives the question and retrieved context, then generates a natural-language answer.
The model does not need to be trained separately on every uploaded subject. Instead, relevant information is supplied dynamically through retrieval.

Step 11 — Return the response
FastAPI returns the generated answer to the frontend, where it is displayed to the user.
Where available, the application can also display source filenames and page references to help users verify the answer.

Why Use RAG?

Retrieval-Augmented Generation combines information retrieval with language generation.
Without retrieval, a language model primarily relies on information learned during training and the prompt supplied at inference time. With RAG, the application retrieves relevant information from its document collection and supplies that information as context.

Benefits include:

1] Answers grounded in the uploaded material.
2] Support for changing document collections without retraining the LLM.
3] Semantic search across lengthy documents.
4] The ability to provide document references when source metadata is retained.
5] A modular architecture in which the LLM, embedding model, and vector database can be changed independently when compatible.

RAG reduces reliance on the model's general knowledge for document-specific answers, but it does not guarantee that every answer will be correct
