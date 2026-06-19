import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()


import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("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"))

# -----------------------------
# Load Documents
# -----------------------------
def load_documents(docs_path="docs"):
    print(f"\nLoading documents from '{docs_path}'...\n")

    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"{docs_path} folder does not exist.")

    documents = []

    files = [f for f in os.listdir(docs_path) if f.endswith(".txt")]

    if not files:
        raise FileNotFoundError("No .txt files found.")

    for file in files:

        file_path = os.path.join(docs_path, file)

        print(f"Loading {file}...")

        try:

            loader = TextLoader(
                file_path,
                encoding="utf-8",
                autodetect_encoding=True
            )

            docs = loader.load()

            documents.extend(docs)

            print(f"✓ Loaded {file}")

        except Exception as e:

            print(f"❌ Failed to load {file}")

            print(e)

    print(f"\nTotal Documents Loaded: {len(documents)}")

    return documents


# -----------------------------
# Split Documents
# -----------------------------
def split_documents(documents):

    print("\nSplitting documents...\n")

    splitter = CharacterTextSplitter(

        separator="\n",

        chunk_size=1000,

        chunk_overlap=200,

        length_function=len

    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks\n")

    return chunks


# -----------------------------
# Create ChromaDB
# -----------------------------
def create_vector_store(chunks):

    print("Creating Embeddings...\n")

    embedding = OpenAIEmbeddings(

        model="text-embedding-3-small"

    )

    vectorstore = Chroma.from_documents(

        documents=chunks,

        embedding=embedding,

        persist_directory="db/chroma_db"

    )

    print("✓ ChromaDB Created Successfully")

    return vectorstore


# -----------------------------
# Main
# -----------------------------
def main():

    print("=" * 50)

    print("RAG INGESTION PIPELINE")

    print("=" * 50)

    persist_directory = "db/chroma_db"

    if os.path.exists(persist_directory):

        print("\nExisting Vector Database Found")

        print("Delete db/chroma_db if you want to re-ingest.\n")

        return

    documents = load_documents()

    chunks = split_documents(documents)

    create_vector_store(chunks)

    print("\nDONE!")


if __name__ == "__main__":

    main()