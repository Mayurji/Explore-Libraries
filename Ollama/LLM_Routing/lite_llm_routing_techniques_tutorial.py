import os
import time
import random
import numpy as np
from sentence_transformers import SentenceTransformer
from litellm import completion
from dotenv import load_dotenv
from prometheus_client import start_http_server, Counter, Histogram, Summary
import pandas as pd


load_dotenv()

# -----------------------------
# CONFIGURATION
# -----------------------------

OLLAMA_MODEL = "ollama/llama3.2"
GEMINI_MODEL = "gemini/gemini-2.5-flash"  # Corrected to a more common model name if needed, but keeping user's choice if it exists

# -----------------------------
# METRICS INITIALIZATION
# -----------------------------

# Request metrics
REQUEST_COUNT = Counter('llm_requests_total', 'Total number of LLM requests', ['model', 'router'])
REQUEST_LATENCY = Histogram('llm_request_duration_seconds', 'Latency of LLM requests in seconds', ['model'])
TOKEN_USAGE = Counter('llm_token_usage_total', 'Token usage (input/output)', ['model', 'token_type'])
ROUTING_DECISIONS = Counter('llm_routing_decisions_total', 'Counts of routing decisions made', ['router', 'model'])
LLM_ERRORS = Counter('llm_errors_total', 'Total number of LLM request errors', ['model', 'error_type'])

# -----------------------------
# HELPER: LLM CALL
# -----------------------------

def call_llm(model, prompt, router_name="none"):
    start_time = time.time()
    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        duration = time.time() - start_time
        
        # Track metrics
        REQUEST_COUNT.labels(model=model, router=router_name).inc()
        REQUEST_LATENCY.labels(model=model).observe(duration)
        
        # Token usage
        usage = response.get('usage', {})
        TOKEN_USAGE.labels(model=model, token_type='prompt').inc(usage.get('prompt_tokens', 0))
        TOKEN_USAGE.labels(model=model, token_type='completion').inc(usage.get('completion_tokens', 0))
        
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        LLM_ERRORS.labels(model=model, error_type=type(e).__name__).inc()
        print(f"Error calling {model}: {e}")
        return f"Error: {e}"

# -----------------------------
# 1. SEMANTIC ROUTING
# -----------------------------

class SemanticRouter:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.routes = {
            "coding": ("Write Python code:", OLLAMA_MODEL),
            "general": ("Explain gravity", GEMINI_MODEL)
        }
        self.embeddings = {
            key: self.embedder.encode(val[0]) for key, val in self.routes.items()
        }

    def route(self, query):
        query_emb = self.embedder.encode(query)
        scores = {
            key: np.dot(query_emb, emb) for key, emb in self.embeddings.items()
        }
        best_route = max(scores, key=scores.get)
        model = self.routes[best_route][1]
        
        # Track routing decision
        ROUTING_DECISIONS.labels(router='semantic', model=model).inc()
        return model

# -----------------------------
# 2. COST-AWARE ROUTING
# -----------------------------

class CostAwareRouter:
    def __init__(self, threshold=100):
        self.threshold = threshold

    def route(self, query):
        if len(query) > self.threshold:
            model = GEMINI_MODEL  # better quality for long queries
        else:
            model = OLLAMA_MODEL  # cheaper
            
        # Track routing decision
        ROUTING_DECISIONS.labels(router='cost_aware', model=model).inc()
        return model

# -----------------------------
# 3. INTENT-BASED ROUTING
# -----------------------------

class IntentRouter:
    def route(self, query):
        if "code" in query.lower():
            model = OLLAMA_MODEL
        elif "explain" in query.lower() or "why" in query.lower():
            model = GEMINI_MODEL
        else:
            model = GEMINI_MODEL
            
        # Track routing decision
        ROUTING_DECISIONS.labels(router='intent', model=model).inc()
        return model

# -----------------------------
# 4. CASCADING ROUTING
# -----------------------------

class CascadingRouter:
    def __init__(self):
        self.models = [OLLAMA_MODEL, GEMINI_MODEL]

    def route(self, query):
        for model in self.models:
            response = call_llm(model, query, router_name="cascading")
            if "Error" not in response and len(response) > 50:  # simple quality check
                ROUTING_DECISIONS.labels(router='cascading', model=model).inc()
                return response
        return "Failed to get good response"

# -----------------------------
# 5. LOAD BALANCING
# -----------------------------

class LoadBalancer:
    def __init__(self):
        self.models = [OLLAMA_MODEL, GEMINI_MODEL]
        self.index = 0

    def route(self, query):
        model = self.models[self.index]
        self.index = (self.index + 1) % len(self.models)
        
        # Track routing decision
        ROUTING_DECISIONS.labels(router='load_balancer', model=model).inc()
        return model

if __name__ == "__main__":
    # Start Prometheus server on port 8001
    print("Starting Prometheus metrics server on port 8001...")
    start_http_server(8001)
    
    # Sample queries to test different routers
    test_queries = [
        "Write a Python function to sort a list",
        "Explain quantum entanglement for a 5 year old",
        "How do I fix a leaking faucet?",
        "What is the capital of France?",
        "Why is the sky blue?",
        "Write a bash script to monitor CPU usage",
        "Explain the theory of relativity"
    ]

    print("\n--- Running Continuous Routing simulation (Ctrl+C to stop) ---")
    
    routers = [
        ("semantic", SemanticRouter()),
        ("cost_aware", CostAwareRouter()),
        ("intent", IntentRouter()),
        ("load_balancer", LoadBalancer())
    ]
    
    try:
        while True:
            # Pick a random router and query
            router_name, router = random.choice(routers)
            query = random.choice(test_queries)
            
            print(f"\n[Router: {router_name}] Query: {query}")
            
            model = router.route(query)
            print(f"Selected Model: {model}")
            
            response = call_llm(model, query, router_name=router_name)
            print(f"Response: {response[:100]}...")
            
            # Wait a bit between calls to avoid hitting rate limits too fast (and to see metrics flow)
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nSimulation stopped.")

