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

## Future Enhancement: Integrated Server Process Management

### Overview
Integrate server process management directly into LADA to automatically handle Ollama and MLX server lifecycle, improving user experience for non-technical users.

### Benefits
- **User Convenience**: Single command to start LADA with all required servers
- **Centralized Logging**: Capture and display server logs within LADA
- **Dynamic Management**: Start/stop servers on demand based on model usage
- **Better Error Handling**: Provide clear feedback when servers fail to start
- **Resource Efficiency**: Stop idle servers to free resources

### Implementation Ideas
1. **Server Manager Module**
   - Process lifecycle management (start, stop, restart)
   - Health monitoring and auto-recovery
   - Port conflict resolution
   - Log aggregation and filtering

2. **CLI Enhancement**
   ```bash
   # Potential new commands
   lada server start    # Start all required servers
   lada server stop     # Stop managed servers
   lada server status   # Show server status
   lada server logs     # Show aggregated logs
   ```

3. **Auto-Start Option**
   - Configuration option to enable/disable auto-start
   - Smart detection of which servers are needed
   - Background process management

### Considerations
- Cross-platform compatibility (MacOS, Linux, Windows)
- Security implications of process management
- Handling existing server instances
- Resource usage and performance impact
- Graceful shutdown and cleanup

### Priority
Low - Focus on core functionality first. This enhancement can be added later based on user feedback and adoption patterns.
