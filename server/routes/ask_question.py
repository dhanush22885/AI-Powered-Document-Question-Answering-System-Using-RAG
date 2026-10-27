
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from pydantic import PrivateAttr
from typing import List
from logger import logger
import os

router = APIRouter()


@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"User query: {question}")

        # Validate environment variables
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        index_name = os.getenv("PINECONE_INDEX_NAME")
        google_api_key = os.getenv("GOOGLE_API_KEY")

        if not pinecone_api_key or not index_name:
            raise ValueError(
                "PINECONE_API_KEY or PINECONE_INDEX_NAME is missing"
            )

        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY is missing")

        # Connect to Pinecone
        pc = Pinecone(api_key=pinecone_api_key)
        index = pc.Index(index_name)

        # Initialize embedding model with 768 dimensions
        embed_model = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=google_api_key,
            output_dimensionality=768
        )

        # Generate query embedding
        embedded_query = embed_model.embed_query(question)

        # Debug information
        logger.info(
            f"Embedding model: {embed_model.model}"
        )
        logger.info(
            f"Query embedding dimension: {len(embedded_query)}"
        )
        logger.info(
            f"Pinecone index name: {index_name}"
        )

        # Verify dimensions before querying Pinecone
        if len(embedded_query) != 768:
            raise ValueError(
                f"Expected 768-dimensional query vector, "
                f"but got {len(embedded_query)}. "
                "Check the langchain-google-genai package version."
            )

        # Query Pinecone
        res = index.query(
            vector=embedded_query,
            top_k=3,
            include_metadata=True
        )

        # Convert Pinecone matches into LangChain documents
        docs = [
            Document(
                page_content=match.get("metadata", {}).get("text", ""),
                metadata=match.get("metadata", {})
            )
            for match in res.get("matches", [])
        ]

        if not docs:
            return {
                "answer": (
                    "I couldn't find relevant information "
                    "in the uploaded documents."
                ),
                "source_documents": []
            }

        # Custom retriever
        class SimpleRetriever(BaseRetriever):
            _docs: List[Document] = PrivateAttr(
                default_factory=list
            )

            def __init__(self, documents: List[Document]):
                super().__init__()
                self._docs = documents

            def _get_relevant_documents(
                self, query: str
            ) -> List[Document]:
                return self._docs

        retriever = SimpleRetriever(docs)

        # Generate answer using the LLM chain
        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)

        logger.info("Query successful")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
