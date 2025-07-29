"""
MLX FastAPI Server for LADA.

This server provides an Ollama-compatible API for MLX models.
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from lada.servers.mlx_wrapper import MLXModelWrapper, GenerationConfig

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MLX Server for LADA", version="0.1.0")
model_wrapper = MLXModelWrapper()


class GenerateRequest(BaseModel):
    """Request format matching Ollama's /api/generate endpoint."""
    model: str
    prompt: str
    system: Optional[str] = None
    template: Optional[str] = None
    options: Optional[Dict] = Field(default_factory=dict)
    stream: bool = False


class GenerateResponse(BaseModel):
    """Response format matching Ollama's /api/generate endpoint."""
    model: str
    created_at: str
    response: str
    done: bool = True
    total_duration: int
    load_duration: int = 0
    prompt_eval_count: int
    eval_count: int
    eval_duration: int


class Model(BaseModel):
    """Model information format."""
    name: str
    modified_at: str
    size: str
    digest: str = "unknown"
    details: Dict = Field(default_factory=dict)


class TagsResponse(BaseModel):
    """Response for /api/tags endpoint."""
    models: List[Model]


@app.get("/api/tags")
async def list_models() -> TagsResponse:
    """List available models in Ollama-compatible format."""
    models = []
    for model_name in model_wrapper.list_models():
        info = model_wrapper.get_model_info(model_name)
        models.append(Model(
            name=model_name,
            modified_at=datetime.now().isoformat(),
            size=info["size"],
            details={
                "is_loaded": info["is_loaded"],
                "is_downloaded": info["is_downloaded"],
                "model_id": info["model_id"]
            }
        ))
    return TagsResponse(models=models)


@app.post("/api/generate")
async def generate(request: GenerateRequest) -> GenerateResponse:
    """Generate text completion in Ollama-compatible format."""
    # Load model if needed
    if model_wrapper.current_model_name != request.model:
        success, message = model_wrapper.load_model(request.model)
        if not success:
            raise HTTPException(status_code=404, detail=message)
    
    # Extract generation options
    options = request.options or {}
    config = GenerationConfig(
        max_tokens=options.get("num_predict", 2048),
        temperature=options.get("temperature", 0.7),
        top_p=options.get("top_p", 0.95),
        repetition_penalty=options.get("repetition_penalty", 1.1),
        seed=options.get("seed", None)
    )
    
    # Combine system prompt if provided
    prompt = request.prompt
    if request.system:
        prompt = f"{request.system}\n\n{prompt}"
    
    try:
        # Generate response
        response_text, metadata = model_wrapper.generate(prompt, config)
        
        # Convert times to nanoseconds for Ollama compatibility
        total_duration_ns = int(metadata["generation_time"] * 1e9)
        eval_duration_ns = int(metadata["generation_time"] * 1e9)
        
        return GenerateResponse(
            model=request.model,
            created_at=datetime.now().isoformat(),
            response=response_text,
            done=True,
            total_duration=total_duration_ns,
            prompt_eval_count=metadata["prompt_tokens"],
            eval_count=metadata["completion_tokens"],
            eval_duration=eval_duration_ns
        )
        
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Check server health."""
    return {
        "status": "healthy",
        "current_model": model_wrapper.current_model_name,
        "available_models": len(model_wrapper.list_models())
    }


@app.post("/api/load")
async def load_model(model_name: str) -> Dict:
    """Explicitly load a model."""
    success, message = model_wrapper.load_model(model_name)
    if not success:
        raise HTTPException(status_code=404, detail=message)
    return {"status": "success", "message": message}


@app.post("/api/unload")
async def unload_model() -> Dict:
    """Unload the current model."""
    model_wrapper.unload_model()
    return {"status": "success", "message": "Model unloaded"}


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MLX Server for LADA")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    
    args = parser.parse_args()
    
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    logger.info(f"Starting MLX server on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)
