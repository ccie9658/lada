# TODO

## MLX Parameter Review and Feature Parity

### Current Status
- ✅ MLX Server successfully implemented with basic generation support
- ✅ Ollama-compatible API endpoints working
- ❌ Advanced parameters not supported (temperature, top_p, repetition_penalty, seed)

### Tasks

#### 1. Research MLX Parameter Support
- [ ] Deep dive into MLX documentation for generation parameters
- [ ] Check MLX GitHub issues/discussions for parameter support
- [ ] Review mlx-lm source code for hidden/undocumented parameters
- [ ] Test different MLX versions to see if newer versions support more parameters

#### 2. Parameter Comparison Study
- [ ] Create comprehensive table comparing Ollama vs MLX parameters:
  - Ollama: temperature, top_p, top_k, repeat_penalty, seed, num_predict, etc.
  - MLX: Currently only max_tokens confirmed working
- [ ] Document parameter equivalents or workarounds
- [ ] Identify which parameters are critical vs nice-to-have

#### 3. Implementation Strategies
- [ ] Investigate if MLX `stream_generate` function accepts more parameters
- [ ] Check if parameters can be passed through tokenizer config
- [ ] Explore MLX model configuration options
- [ ] Consider implementing parameter emulation at server level

#### 4. Feature Parity Improvements
- [ ] Implement any discovered parameters in MLX wrapper
- [ ] Add parameter validation and helpful error messages
- [ ] Update documentation with parameter support matrix
- [ ] Create fallback strategies for unsupported parameters

#### 5. Testing and Validation
- [ ] Create parameter test suite for MLX models
- [ ] Compare output quality with/without parameters
- [ ] Benchmark performance impact of different parameters
- [ ] Validate consistency between Ollama and MLX outputs

### Notes
- Current MLX version might have limited parameter support by design
- Apple's MLX framework is still evolving, check for updates regularly
- Consider reaching out to MLX community for parameter guidance

### References
- MLX GitHub: https://github.com/ml-explore/mlx
- MLX-LM: https://github.com/ml-explore/mlx-examples/tree/main/llms
- Ollama API: https://github.com/ollama/ollama/blob/main/docs/api.md
