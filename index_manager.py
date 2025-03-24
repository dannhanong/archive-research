from tools import fetch_arxiv_papers
from llama_index.core import Document
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage

class IndexManager:
    def __init__(self, embed_model):
        self.embed_model = embed_model
        self.papers = []

    def fetch_papers(self, topic, papers_count=10):
        self.papers = fetch_arxiv_papers(topic, papers_count)

    def create_documents_from_papers(self):
        for paper in self.papers:
            content = (
                f'Title: {paper["title"]}\n'
                f'Authors: {", ".join(paper["authors"])}\n'
                f'Summary: {paper["summary"]}\n'
                f'Published: {paper["published"]}\n'
                f'Journal reference: {paper["journal_ref"]}\n'
                f'DOI: {paper["doi"]}\n'
                f'Primary category: {paper["primary_category"]}\n'
                f'Categories: {", ".join(paper["categories"])}\n'
                f'PDF URL: {paper["pdf_url"]}\n'
            )
            self.documents.append(Document(text=content))

    def create_index(self):
        self.documents = []
        self.create_documents_from_papers()
        Settings.chunk_size=1024
        Settings.chunk_overlap=50
        self.index = VectorStoreIndex.from_documents(self.documents, embed_model=self.embed_model)

    def retrieve_index(self):
        storage_context = StorageContext.from_defaults(persist_dir="index/")
        self.index = load_index_from_storage(storage_context, emded_model = self.embed_model)

    def list_papers(self):
        print([paper['title'] for paper in self.papers])
