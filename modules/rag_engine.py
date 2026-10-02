"""
RAG (Retrieval-Augmented Generation) Engine for Doc-Mind AI
Provides vector indexing, semantic search, and grounded context retrieval.
"""
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import RAG_TOP_K


class RAGEngine:
    def __init__(self, chunks: Optional[List[Dict[str, Any]]] = None):
        self.chunks = chunks or []
        self.vectorizer = None
        self.tfidf_matrix = None
        if self.chunks:
            self._build_index()

    def set_chunks(self, chunks: List[Dict[str, Any]]):
        """Indexes new chunks."""
        self.chunks = chunks
        self._build_index()

    def _build_index(self):
        """Builds TF-IDF semantic index over document chunks."""
        if not self.chunks:
            self.vectorizer = None
            self.tfidf_matrix = None
            return

        corpus = [chunk["text"] for chunk in self.chunks]
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=10000,
            sublinear_tf=True,
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def retrieve(self, query: str, top_k: int = RAG_TOP_K) -> List[Dict[str, Any]]:
        """
        Retrieves top_k most relevant chunks for a query with similarity scores.
        """
        if not self.chunks or self.vectorizer is None or self.tfidf_matrix is None:
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        # Sort indices in descending order
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            chunk = dict(self.chunks[idx])
            chunk["similarity_score"] = round(score, 4)
            results.append(chunk)

        return results

    def query_with_llm(
        self,
        query: str,
        gemini_client,
        top_k: int = RAG_TOP_K,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves context chunks and prompts Gemini for a grounded answer.
        """
        retrieved_chunks = self.retrieve(query, top_k=top_k)

        if not gemini_client or not gemini_client.is_configured:
            # Fallback when API key is not yet provided
            best_chunk = retrieved_chunks[0] if retrieved_chunks else None
            fallback_text = (
                "⚠️ **Gemini API Key Required**: Please enter your Gemini API Key in the left sidebar "
                "to enable AI-grounded conversational answers.\n\n"
            )
            if best_chunk:
                fallback_text += (
                    f"**Most Relevant Document Excerpt (Page {best_chunk.get('page', 'N/A')}):**\n\n"
                    f"> {best_chunk.get('text', '')[:400]}..."
                )
            return {
                "answer": fallback_text,
                "retrieved_chunks": retrieved_chunks,
                "model_used": "Offline Search Index",
            }

        try:
            answer = gemini_client.rag_query(query, retrieved_chunks, chat_history)
            return {
                "answer": answer,
                "retrieved_chunks": retrieved_chunks,
                "model_used": gemini_client.model_name,
            }
        except Exception as e:
            err_msg = str(e)
            best_chunk = retrieved_chunks[0] if retrieved_chunks else None
            fallback_text = f"⚠️ **AI Chat Warning**: {err_msg}\n\n"
            if best_chunk:
                fallback_text += (
                    f"**Most Relevant Document Excerpt (Page {best_chunk.get('page', 'N/A')}):**\n\n"
                    f"> {best_chunk.get('text', '')[:400]}..."
                )
            return {
                "answer": fallback_text,
                "retrieved_chunks": retrieved_chunks,
                "model_used": "Semantic Search Fallback",
            }
