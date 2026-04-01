from semantic_router.routers import SemanticRouter
import json

config_path = "/home/mayur/Documents/git-repo-with-ads/Explore-Libraries/Ollama/liteLLM_Ollama/router.json"
try:
    router = SemanticRouter.from_json(config_path)
    print("Successfully loaded router from JSON")
    print(f"Routes: {router.routes}")
except Exception as e:
    print(f"Error loading router: {e}")
    import traceback
    traceback.print_exc()
