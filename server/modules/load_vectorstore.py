
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME", "medicalindex"
)

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing from .env")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing from .env")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)

existing_indexes = pc.list_indexes().names()

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        metric="dotproduct",
        spec=spec
    )

    while not pc.describe_index(
        PINECONE_INDEX_NAME
    ).status["ready"]:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)

# Load, split, embed, and upload PDF documents
def load_vectorstore(uploaded_files):

    # IMPORTANT: Generate 768-dimensional embeddings
    embed_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
        output_dimensionality=768
    )

    file_paths = []

    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / Path(file.filename).name

        with open(save_path, "wb") as f:
            f.write(file.file.read())

        file_paths.append(str(save_path))

    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(documents)

        if not chunks:
            print(f"No text extracted from {file_path}")
            continue

        texts = [chunk.page_content for chunk in chunks]

        # Include the document text in Pinecone metadata
        metadatas = [
            {
                **chunk.metadata,
                "text": chunk.page_content
            }
            for chunk in chunks
        ]

        ids = [
            f"{Path(file_path).stem}-{i}"
            for i in range(len(chunks))
        ]

        print(f"Embedding {len(texts)} chunks...")

        embeddings = embed_model.embed_documents(texts)

        # Verify dimensions before uploading
        dimensions = {len(vector) for vector in embeddings}
        print(f"Embedding dimensions generated: {dimensions}")

        if dimensions != {768}:
            raise ValueError(
                f"Expected 768-dimensional embeddings, "
                f"but received dimensions: {dimensions}"
            )

        print("Uploading vectors to Pinecone...")

        vectors = [
            (ids[i], embeddings[i], metadatas[i])
            for i in range(len(embeddings))
        ]

        for start in tqdm(
            range(0, len(vectors), 100),
            desc="Upserting to Pinecone"
        ):
            index.upsert(vectors=vectors[start:start + 100])

        print(f"Upload complete for {file_path}")

    return {"message": "PDF processing completed"}
