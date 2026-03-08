# basic_rag.py
from langchain_community.document_loaders import TextLoader  # Or PyPDFLoader for PDFs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Load the document (replace with your file path)
loader = TextLoader("sample_sv_doc.txt")  # For text files; see PDF note below
documents = loader.load()
print(f"Loaded {len(documents)} documents.")

# 2. Split into chunks (default settings: ~1000 chars/chunk, 200 overlap)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks.")

# 3. Set up embeddings (using Ollama local model)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 4. Create vector store (ChromaDB) and add chunks
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="sv_docs"  # Name for your collection; persists locally in ./chroma_db
)

# 5. Set up retriever (fetches top 4 similar chunks by default)
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

# 6. Set up LLM (Ollama local model)
llm = ChatOllama(model="llama3")

# 7. Define prompt template (instructs LLM to use only retrieved context)
prompt = ChatPromptTemplate.from_template(
    """
    You are an expert in SystemVerilog. Answer the question based only on the following context:
    {context}

    Question: {question}
    """
)

# 8. Format retrieved docs for the prompt
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 9. Build the RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 10. Run a test query
query = "Explain the adder module."
response = rag_chain.invoke(query)
print("Response:", response)