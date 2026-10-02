"""
Gemini API Client Wrapper for Doc-Mind AI
High-reliability REST integration for Google Gemini API.
Features automatic model sanitization (targeting gemini-1.5-flash),
direct structured JSON extraction, and grounded RAG query generation.
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
import requests

from config import DEFAULT_GEMINI_MODEL, FALLBACK_GEMINI_MODELS

# Default production model preference order
PREFERRED_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-pro", "gemini-1.5-pro"]


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None, model_name: str = DEFAULT_GEMINI_MODEL):
        self.api_key = (api_key or os.getenv("GEMINI_API_KEY", "")).strip()
        self.model_name = self._clean_model_name(model_name)
        self.available_models: List[str] = []

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def _clean_model_name(self, name: str) -> str:
        """Strips 'models/' prefix and whitespace from model identifier."""
        if not name:
            return "gemini-2.5-flash"
        m = name.strip()
        if m.startswith("models/"):
            m = m[len("models/"):]
        return m

    def _sanitize_error(self, err: Any) -> str:
        """Sanitizes error messages so API keys are never exposed in UI or logs."""
        msg = str(err)
        if self.api_key:
            msg = msg.replace(self.api_key, "******")
        msg = re.sub(r"key=[a-zA-Z0-9_\-]+", "key=******", msg)

        if "401" in msg or "ACCESS_TOKEN_TYPE_UNSUPPORTED" in msg or "invalid authentication credentials" in msg.lower():
            return "Invalid key format (rejected by Google: ACCESS_TOKEN_TYPE_UNSUPPORTED). Please obtain a standard Gemini API key starting with 'AIzaSy' from Google AI Studio (https://aistudio.google.com/app/apikey)."
        if "400" in msg or "403" in msg:
            if "API_KEY_INVALID" in msg or "key not valid" in msg.lower():
                return "Invalid Gemini API Key. Please verify your key from Google AI Studio (https://aistudio.google.com/app/apikey). Standard keys start with 'AIzaSy'."
            if "has not been used in project" in msg or "disabled" in msg.lower():
                return "Generative Language API is disabled in your Google Cloud Project. Please enable it in Google Cloud Console or create a free key in Google AI Studio."
            return f"Unauthorized or invalid API request. Please verify your Gemini API key from Google AI Studio."
        if "429" in msg:
            return "Gemini API rate limit or quota exceeded. Please wait a moment or check your Google AI Studio quota."
        return msg

    def _call_gemini_api(self, prompt: str, system_instruction: Optional[str] = None, response_json: bool = False, model_name: Optional[str] = None) -> str:
        """Performs a direct, high-reliability REST call to Google Gemini API."""
        if not self.is_configured:
            raise ValueError("Gemini API key is required.")

        target_model = self._clean_model_name(model_name or self.model_name)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={self.api_key}"

        payload: Dict[str, Any] = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        gen_cfg: Dict[str, Any] = {"temperature": 0.2}
        if response_json:
            gen_cfg["responseMimeType"] = "application/json"
        payload["generationConfig"] = gen_cfg

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }

        try:
            res = requests.post(url, json=payload, headers=headers, timeout=45)
        except Exception as net_err:
            raise RuntimeError(self._sanitize_error(f"Network error contacting Gemini API: {net_err}"))

        if res.status_code != 200:
            err_msg = ""
            try:
                err_data = res.json().get("error", {})
                err_msg = err_data.get("message", res.text)
            except Exception:
                err_msg = res.text
            sanitized = self._sanitize_error(f"HTTP {res.status_code}: {err_msg}")
            raise RuntimeError(sanitized)

        data = res.json()
        candidates = data.get("candidates", [])
        if candidates and "content" in candidates[0]:
            parts = candidates[0]["content"].get("parts", [])
            if parts and "text" in parts[0]:
                return parts[0]["text"]

        block_reason = data.get("promptFeedback", {}).get("blockReason")
        if block_reason:
            raise RuntimeError(f"Gemini generation blocked by safety filters: {block_reason}")

        return ""

    def test_connection(self) -> Dict[str, Any]:
        """
        Dynamically verifies the API key by querying Google's ModelService
        and testing content generation on an active available model.
        """
        if not self.is_configured:
            return {"success": False, "error": "API Key is not configured."}

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }

        # Step 1: Discover available models for this specific API key
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
        available: List[str] = []
        try:
            list_res = requests.get(list_url, headers=headers, timeout=12)
            if list_res.status_code != 200:
                err_json = {}
                try:
                    err_json = list_res.json().get("error", {})
                except Exception:
                    pass
                err_code = err_json.get("code", list_res.status_code)
                err_msg = err_json.get("message", list_res.text)
                return {"success": False, "error": self._sanitize_error(f"HTTP {err_code}: {err_msg}")}

            data = list_res.json()
            for m in data.get("models", []):
                methods = m.get("supportedGenerationMethods", [])
                if "generateContent" in methods:
                    name = m.get("name", "").replace("models/", "").strip()
                    if name:
                        available.append(name)

        except Exception as net_err:
            return {"success": False, "error": self._sanitize_error(f"Connection failed: {net_err}")}

        if not available:
            return {"success": False, "error": "No generateContent-capable models available for this key."}

        self.available_models = available

        # Step 2: Prioritize candidates based on user preference and active availability
        candidates = []
        # First preference: current requested model if available
        if self.model_name in available:
            candidates.append(self.model_name)

        # Standard priority models if present in available list
        for p in PREFERRED_MODELS:
            clean_p = self._clean_model_name(p)
            if clean_p in available and clean_p not in candidates:
                candidates.append(clean_p)

        # Any remaining flash models
        for m in available:
            if "flash" in m and m not in candidates:
                candidates.append(m)

        # Any remaining models
        for m in available:
            if m not in candidates:
                candidates.append(m)

        # Step 3: Run live test generation on top candidate
        last_error = None
        for candidate in candidates[:3]:
            test_url = f"https://generativelanguage.googleapis.com/v1beta/models/{candidate}:generateContent?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": "Respond with 'Doc-Mind AI Online'"}]}]}

            try:
                res = requests.post(test_url, json=payload, headers=headers, timeout=12)
                if res.status_code == 200:
                    self.model_name = candidate
                    return {
                        "success": True,
                        "model": candidate,
                        "available_models": available,
                        "response": "Doc-Mind AI Online",
                    }

                err_json = {}
                try:
                    err_json = res.json().get("error", {})
                except Exception:
                    pass
                err_code = err_json.get("code", res.status_code)
                err_msg = err_json.get("message", res.text)
                last_error = f"HTTP {err_code}: {err_msg}"

            except Exception as e:
                last_error = str(e)

        return {"success": False, "error": self._sanitize_error(last_error or "Failed to generate content with available models.")}

    def generate_json(self, prompt: str, system_instruction: Optional[str] = None) -> Dict[str, Any]:
        """Generates content and parses output as a Python dictionary (JSON)."""
        # Try structured JSON output first
        try:
            raw_text = self._call_gemini_api(prompt, system_instruction=system_instruction, response_json=True)
            return self._clean_json(raw_text)
        except Exception as first_err:
            # If application/json mode failed, retry with normal text mode + explicit JSON instruction
            try:
                retry_prompt = f"{prompt}\n\nCRITICAL REQUIREMENT: Output valid, parseable JSON only. Do not wrap in markdown or commentary."
                raw_text = self._call_gemini_api(retry_prompt, system_instruction=system_instruction, response_json=False)
                return self._clean_json(raw_text)
            except Exception:
                raise first_err

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generates plain markdown/text response."""
        return self._call_gemini_api(prompt, system_instruction=system_instruction, response_json=False)

    def rag_query(self, query: str, context_chunks: List[Dict[str, Any]], chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """Answers a user's question grounded in retrieved document chunks."""
        system_prompt = (
            "You are Doc-Mind AI, an intelligent document analysis assistant. "
            "Your task is to provide accurate, concise, and helpful answers strictly based on the provided context. "
            "If the context does not contain enough information, state clearly that the document does not mention it, "
            "and suggest what related details might be present. "
            "Include specific page references whenever provided in the context."
        )

        formatted_context = ""
        for i, chunk in enumerate(context_chunks, 1):
            source = chunk.get("source", f"Chunk {i}")
            page = chunk.get("page", "N/A")
            text = chunk.get("text", "")
            formatted_context += f"\n--- Context Snippet {i} [Source: {source} | Page: {page}] ---\n{text}\n"

        conversation = ""
        if chat_history:
            recent = chat_history[-6:]
            for msg in recent:
                role = "User" if msg.get("role") == "user" else "Doc-Mind AI"
                conversation += f"{role}: {msg.get('content')}\n"

        prompt = f"""
DOCUMENT RETRIEVED CONTEXT:
{formatted_context}

PREVIOUS CHAT (if any):
{conversation}

USER QUESTION:
{query}

Please provide a well-structured, clear, markdown-formatted response based strictly on the context above.
"""
        return self.generate_text(prompt, system_instruction=system_prompt)

    def _clean_json(self, raw_text: str) -> Dict[str, Any]:
        """Cleans and extracts JSON object or array from model response."""
        if not raw_text or not raw_text.strip():
            raise ValueError("Gemini returned empty response text.")

        text = raw_text.strip()

        # 1. Try markdown code block extraction (```json ... ``` or ``` ... ```)
        code_block = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if code_block:
            snippet = code_block.group(1).strip()
            try:
                return json.loads(snippet)
            except Exception:
                fixed = re.sub(r",\s*([\]}])", r"\1", snippet)
                try:
                    return json.loads(fixed)
                except Exception:
                    pass

        # 2. Try direct parse of raw text
        try:
            return json.loads(text)
        except Exception:
            pass

        # 3. Try regex extraction of first outer { ... }
        obj_match = re.search(r"(\{[\s\S]*\})", text)
        if obj_match:
            candidate = obj_match.group(1).strip()
            try:
                return json.loads(candidate)
            except Exception:
                fixed = re.sub(r",\s*([\]}])", r"\1", candidate)
                try:
                    return json.loads(fixed)
                except Exception:
                    pass

        # 4. Try regex extraction of first outer [ ... ]
        arr_match = re.search(r"(\[[\s\S]*\])", text)
        if arr_match:
            candidate = arr_match.group(1).strip()
            try:
                return json.loads(candidate)
            except Exception:
                fixed = re.sub(r",\s*([\]}])", r"\1", candidate)
                try:
                    return json.loads(fixed)
                except Exception:
                    pass

        raise ValueError(f"Could not parse valid JSON from Gemini output: {text[:200]}...")
