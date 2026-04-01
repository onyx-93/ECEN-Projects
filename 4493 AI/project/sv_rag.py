from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import datetime
import os

# ====================== SETUP ======================
os.makedirs("./knowledge_base", exist_ok=True)
print("✅ knowledge_base folder ready (including src/SV subfolder).")

# ====================== 1. LOAD DOCUMENTS ======================
# Load PDFs
pdf_loader = DirectoryLoader(
    path="./knowledge_base",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
    show_progress=True,
    silent_errors=True,
)

# Load text/SystemVerilog files (recursive)
text_loader = DirectoryLoader(
    path="./knowledge_base",
    glob="**/*",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
    show_progress=True,
    silent_errors=True,
)

print("Loading PDFs...")
pdf_docs = pdf_loader.load()

print("Loading SystemVerilog and text files...")
text_docs = text_loader.load()

documents = pdf_docs + text_docs
print(f"✅ Loaded {len(documents)} documents (including files from src/SV and sample_sv_doc.txt).")

if len(documents) == 0:
    print("\nNo documents found!")
    print("Please add files to './knowledge_base' (e.g. your HW5 PDF or .sv files)")
    exit(1)

# ====================== 2. CHUNKING ======================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=120,
    separators=["\n\n", "\nmodule ", "\nendmodule", "\n//", "\n/*", "\n    ", "\n", " ", ""]
)

chunks = text_splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks.")

# ====================== 3. VECTOR STORE ======================
embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="sv_docs",
    persist_directory="./chroma_db"
)

print("✅ Vector database built successfully.")

# ====================== 4. RAG SETUP ======================
retriever = vector_store.as_retriever(search_kwargs={"k": 6})

llm = ChatOllama(model="llama3:8b", temperature=0.1)

prompt = ChatPromptTemplate.from_template(
    """
You are an expert SystemVerilog hardware design engineer.
Generate clean, synthesizable, professional RTL code.

Strict Rules for all code:
- Start with `module name (...);` and end with `endmodule`
- Use `input logic` and `output logic` for ports
- Use `logic` for internal signals
- For gates and simple combinational logic, use continuous `assign`
- Never use #delays, initial blocks for combo logic, or non-synthesizable constructs
- Keep the design minimal and readable

Context (use when helpful):
{context}

Question: {question}

Return the complete module and a short explanation.
"""
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ====================== 5. INTERACTIVE LOOP ======================
print("\n✅ SystemVerilog RAG System is ready!")
print("You can now ask for any module or gate.")
print("Example: Write a single 2-input AND gate module in SystemVerilog")
print("Type 'quit' to exit.\n")

while True:
    query = input("Write a your question: ").strip()
    
    if query.lower() in ['quit', 'q', 'exit']:
        print("Goodbye!")
        break
    
    if not query:
        continue

    print("\nGenerating response...\n")
    response = rag_chain.invoke(query)

    print("Response:")
    print(response)
    print("-" * 90)

    # Logging
    with open("rag_responses_log.txt", "a", encoding="utf-8") as f:
        f.write(f"┌────────────────────────────────────────────────────────────┐\n")
        f.write(f"Query: {query}\n")
        f.write(f"Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"─ Response ─────────────────────────────────────────────────\n")
        f.write(response.strip() + "\n")
        f.write(f"└────────────────────────────────────────────────────────────┘\n\n")

    print(f"Response saved to rag_responses_log.txt\n")