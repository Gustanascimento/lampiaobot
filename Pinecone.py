import openai
from openai.embeddings_utils import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import pinecone

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from dotenv import load_dotenv
load_dotenv()

class PineconeEmbedder():
    def __init__(self) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")

              
    def embed_sentences(self, original_prompt, answers):
        
        usernames = list(answers.keys())
        comparison_phrases = list(answers.values())

        reference_embedding = openai.Embedding.create(input=original_prompt, engine=embedding_model)['data'][0]['embedding']

        comparison_embeddings = [openai.Embedding.create(input=phrase, engine=embedding_model)['data'][0]['embedding'] for phrase in comparison_phrases]
        
        # Calcular a similaridade de cosseno entre o embedding de referência e os embeddings de comparação
        similarity_scores = cosine_similarity(np.array(reference_embedding).reshape(1, -1), np.array(comparison_embeddings))

        scores = list(similarity_scores[0])

        # Encontrar o índice da frase mais similar
        most_similar_index = np.argmax(similarity_scores)

        # Recuperar a frase mais similar de comparison_phrases
        most_similar_phrase = comparison_phrases[most_similar_index]

        results = []

        for player, phrase, pontuacao in zip(usernames, comparison_phrases, scores):
            results.append((player, phrase, pontuacao))

        print("Frase mais similar: ", most_similar_phrase)

        results = sorted(results, key=lambda x: x[2], reverse=True)
        return results
