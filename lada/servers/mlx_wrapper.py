"""
MLX Model Wrapper for LADA.

This module handles loading and running MLX models, providing
a clean interface for the FastAPI server.
"""

import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import mlx_lm
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)


@dataclass
class GenerationConfig:
    """Configuration for text generation."""
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.95
    repetition_penalty: float = 1.1
    seed: Optional[int] = None


class MLXModelWrapper:
    """Wrapper for MLX models providing a simple interface."""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.current_model_name = None
        self._available_models = {
            # Map friendly names to Hugging Face model IDs
            "Qwen2.5-0.5B-Instruct": "mlx-community/Qwen2.5-0.5B-Instruct-4bit",
            "Qwen2.5-1.5B-Instruct": "mlx-community/Qwen2.5-1.5B-Instruct-4bit",
            "Qwen2.5-3B-Instruct": "mlx-community/Qwen2.5-3B-Instruct-4bit",
            "Llama-3.2-1B-Instruct": "mlx-community/Llama-3.2-1B-Instruct-4bit",
            "Llama-3.2-3B-Instruct": "mlx-community/Llama-3.2-3B-Instruct-4bit",
            "GLM-4.5-Air": "mlx-community/glm-4-9b-chat-4bit",  # Placeholder - update when available
        }
    
    def list_models(self) -> List[str]:
        """List available model names."""
        return list(self._available_models.keys())
    
    def get_model_info(self, model_name: str) -> Dict[str, any]:
        """Get information about a specific model."""
        if model_name not in self._available_models:
            return None
            
        # Check if model is downloaded
        cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
        model_id = self._available_models[model_name]
        model_cache_name = f"models--{model_id.replace('/', '--')}"
        is_downloaded = (cache_dir / model_cache_name).exists()
        
        return {
            "name": model_name,
            "model_id": model_id,
            "is_loaded": self.current_model_name == model_name,
            "is_downloaded": is_downloaded,
            "size": self._estimate_model_size(model_name),
        }
    
    def _estimate_model_size(self, model_name: str) -> str:
        """Estimate model size based on name."""
        if "0.5B" in model_name:
            return "~400MB"
        elif "1B" in model_name:
            return "~800MB"
        elif "1.5B" in model_name:
            return "~1.2GB"
        elif "3B" in model_name:
            return "~2.4GB"
        elif "9B" in model_name or "9b" in model_name:
            return "~7GB"
        else:
            return "Unknown"
    
    def load_model(self, model_name: str) -> Tuple[bool, str]:
        """
        Load a model by name.
        
        Returns:
            Tuple of (success, message)
        """
        if model_name not in self._available_models:
            return False, f"Model '{model_name}' not found. Available models: {', '.join(self.list_models())}"
        
        if self.current_model_name == model_name:
            return True, f"Model '{model_name}' already loaded"
        
        try:
            logger.info(f"Loading model: {model_name}")
            model_id = self._available_models[model_name]
            
            # Unload current model if any
            if self.model is not None:
                logger.info(f"Unloading current model: {self.current_model_name}")
                self.model = None
                self.tokenizer = None
                self.current_model_name = None
            
            # Load new model
            start_time = time.time()
            self.model, self.tokenizer = mlx_lm.load(model_id)
            load_time = time.time() - start_time
            
            self.current_model_name = model_name
            logger.info(f"Model loaded successfully in {load_time:.1f}s")
            
            return True, f"Model '{model_name}' loaded successfully in {load_time:.1f}s"
            
        except Exception as e:
            logger.error(f"Failed to load model '{model_name}': {e}")
            return False, f"Failed to load model: {str(e)}"
    
    def generate(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None
    ) -> Tuple[str, Dict[str, any]]:
        """
        Generate text from a prompt.
        
        Returns:
            Tuple of (generated_text, metadata)
        """
        if self.model is None:
            raise ValueError("No model loaded. Call load_model() first.")
        
        if config is None:
            config = GenerationConfig()
        
        try:
            start_time = time.time()
            
            # Generate text
            # Note: MLX doesn't support temperature, top_p, etc. in the current version
            # We'll just use max_tokens for now
            response = mlx_lm.generate(
                self.model,
                self.tokenizer,
                prompt=prompt,
                max_tokens=config.max_tokens,
                verbose=False
            )
            
            generation_time = time.time() - start_time
            
            # Calculate tokens (approximate)
            prompt_tokens = len(self.tokenizer.encode(prompt))
            response_tokens = len(self.tokenizer.encode(response))
            
            metadata = {
                "model": self.current_model_name,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": response_tokens - prompt_tokens,
                "total_tokens": response_tokens,
                "generation_time": generation_time,
            }
            
            # Remove the prompt from the response if it's included
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            
            return response, metadata
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise ValueError(f"Generation failed: {str(e)}")
    
    def unload_model(self):
        """Unload the current model to free memory."""
        if self.model is not None:
            logger.info(f"Unloading model: {self.current_model_name}")
            self.model = None
            self.tokenizer = None
            self.current_model_name = None
