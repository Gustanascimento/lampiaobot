import pinecone
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from dotenv import load_dotenv
load_dotenv()

class PineconeEmbedder():
    def __init__(self) -> None:
        self.api_key = os.getenv("PINECONE_API_KEY")
        pinecone.init(api_key=self.api_key, environment="us-central1-gcp")

        self.module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        self.embedder = hub.load(self.module_url)
              
    def embed_sentences(self, original_prompt, answers):
        answers_list = list(answers.values())
        answers_list.append(original_prompt)
        embeddings = self.embedder(answers_list).numpy()

        distances = np.linalg.norm(embeddings - embeddings[len(answers_list)-1], axis=1)

        np.argmin(distances[:-1])
        
        return embeddings   


