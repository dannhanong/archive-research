import arxiv
import requests
import os

client = arxiv.Client()

def fetch_arxiv_papers(title: str, papers_count: int):
    search_query = f'all:{title}'
    search = arxiv.Search(
        query=search_query,
        max_results=papers_count,
        sort_by=arxiv.SortCriterion.Relevance
    )
    papers = []
    results = client.results(search)
    for result in results:
        paper_info = {
            'title': result.title,
            'authors': [author.name for author in result.authors],
            'summary': result.summary,
            'pdf_url': result.pdf_url,
            'doi': result.doi,
            'published': result.published,
            'primary_category': result.primary_category,
            'categories': result.categories,
            'journal_ref': result.journal_ref,
        }
        papers.append(paper_info)

    return papers

def download_pdf(pdf_url: str, output_file_name: str):
    try:
        os.makedirs('papers', exist_ok=True)
        full_output_path = os.path.join('papers', output_file_name)
        response = requests.get(pdf_url)
        response.raise_for_status()
        with open(full_output_path, 'wb') as file:
            file.write(response.content)
        return f'PDF downloaded to {full_output_path}'
    except requests.exceptions.RequestException as e:
        return f'Error downloading PDF: {e}'
    