#!/usr/bin/env python3
"""
Start the MLX server for LADA.

This script provides a convenient way to launch the MLX model server
with various options.
"""

import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path so we can import lada modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from lada.servers.mlx_server import app
import uvicorn


def main():
    parser = argparse.ArgumentParser(
        description="Start the MLX server for LADA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start with default settings
  python scripts/start_mlx_server.py
  
  # Start on a different port
  python scripts/start_mlx_server.py --port 8080
  
  # Start with a pre-loaded model
  python scripts/start_mlx_server.py --load-model "Qwen2.5-0.5B-Instruct"
  
  # Enable debug logging
  python scripts/start_mlx_server.py --log-level DEBUG
"""
    )
    
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind the server to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to (default: 8000)"
    )
    parser.add_argument(
        "--load-model",
        help="Pre-load a model on startup"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    import logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Pre-load model if requested
    if args.load_model:
        logger.info(f"Pre-loading model: {args.load_model}")
        from lada.servers.mlx_wrapper import MLXModelWrapper
        wrapper = MLXModelWrapper()
        success, message = wrapper.load_model(args.load_model)
        if success:
            logger.info(message)
        else:
            logger.error(message)
            sys.exit(1)
    
    # Start the server
    logger.info(f"Starting MLX server on {args.host}:{args.port}")
    logger.info("Press Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            "lada.servers.mlx_server:app",
            host=args.host,
            port=args.port,
            log_level=args.log_level.lower(),
            reload=args.reload
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
