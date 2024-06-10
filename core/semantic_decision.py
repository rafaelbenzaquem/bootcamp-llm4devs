import numpy as np
from embeddings import embed_msg

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def semantic_decision(user_embedding, table_dictionary):
    max_similarity = -1
    best_table = None
    for table_name in table_dictionary:
        embedding = embed_msg(table_dictionary[table_name])
        similarity = cosine_similarity(user_embedding, embedding)
        if similarity > max_similarity:
            max_similarity = similarity
            best_table = table_name

    return best_table