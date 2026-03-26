from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import datetime

# 1. Load multiple documents with proper handlers
def get_loader_for_file(path: str):
    """Return the correct loader based on file extension"""
    if path.lower().endswith('.pdf'):
        return PyPDFLoader(path)           # Best for PDFs
    else:
        # For .txt, .sv, .md, .v, .vh, etc.
        return TextLoader(path, encoding="utf-8", autodetect_encoding=True)

# Create the DirectoryLoader with custom mapping
loader = DirectoryLoader(
    path="./knowledge_base",                        # ← Put ALL your files in this folder
    glob="**/*.*",                        # Load all files recursively
    show_progress=True,
    use_multithreading=True,
    loader_cls=None,                      # We use custom function instead
    loader_kwargs=None,
    # This applies our custom loader to each file
    custom_loader=get_loader_for_file     # This is the key for mixed types
)

documents = loader.load()
print(f"Loaded {len(documents)} documents from the ./docs folder.")

# 2. Improved Chunking Strategy for SystemVerilog / HDL
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,          # Good balance for code + text
    chunk_overlap=100,
    separators=["\n\n", "\nmodule ", "\nendmodule", "\n//", "\n/*", "\n    ", "\n", " ", "", "_"]
)

chunks = text_splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks.")

# 3. Embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")


# 4. Vector Store with Persistence
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="sv_docs",
    persist_directory="./chroma_db"   # Saves to disk so you don't reload every time
)

# 5. Retriever + LLM + Prompt
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

llm = ChatOllama(model="llama3:8b")

prompt = ChatPromptTemplate.from_template(
    """
    You are an expert SystemVerilog hardware design engineer.
    Answer the question based ONLY on the following context.
    If the context does not contain enough information, say so.

    Context:
    {context}

    Question: {question}
    """
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 6. Interactive Mode + Logging
print("\n✅ RAG System is ready!")
print("You can now ask questions about your project, SystemVerilog code, or any loaded documents.")
print("Type 'quit' to exit.\n")

while True:
    query = input("Your question: ").strip()
    if query.lower() in ['quit', 'q', 'exit']:
        print("Goodbye!")
        break
    if not query:
        continue

    response = rag_chain.invoke(query)
    print("\nResponse:")
    print(response)
    print("-" * 80)

    # Save response to log
    output_file = "rag_responses_log.txt"
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"┌────────────────────────────────────────────────────────────┐\n")
        f.write(f"Query: {query}\n")
        f.write(f"Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"─ Response ─────────────────────────────────────────────────\n")
        f.write(response.strip() + "\n")
        f.write(f"└────────────────────────────────────────────────────────────┘\n\n")

    print(f"Response saved to {output_file}\n")