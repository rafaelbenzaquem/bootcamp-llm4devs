from loader import loadPdf, loadPdfsDirectory
from transformer import transform
from embeddings import embed_docs, embed_msg
from retriever import store, retrieve, test_connection
import numpy as np


pages = loadPdf("../data_sources/Growing Object-Oriented Software, Guided by Tests.pdf")

# pages = loadPdfsDirectory("../data_sources/padroes_discusivas_cebraspe")
#
for page in pages:
    page_transformed = transform(page.page_content)

    print(len(page_transformed))

    page_embedded = embed_docs(page_transformed)

    print(len(page_embedded))

    stored = store(page_transformed, page_embedded, "tdd")

# query = embed_doc("Gostaria do conteúdo básico para concurso do banco central")
# print(query)
# table_name = semantic_decision(query)
# test_connection()
# sources_retrieved = retrieve("content", table_name, query, 3)
# print(sources_retrieved)
