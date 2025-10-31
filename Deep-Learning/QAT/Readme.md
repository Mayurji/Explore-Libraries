### What is Quantization?

Quantization is a model optimization technique that reduces the numerical precision used to represent weights and activations in deep learning models. Its primary benefits include:

Model Compression - lowers memory usage and storage.
Inference Acceleration - speeds up inference and reduces energy consumption.
While quantization is most often used for deployment on edge devices (e.g., phones, embedded hardware), it can also reduce infrastructure costs for large-scale inference in the cloud.

### Weight and Activation Quantization

**Why Quantize Weights?**

Storage savings: Weights are the learned parameters of a model and are saved to disk. Reducing their precision (e.g., from float32 to int8) significantly shrinks the size of the model file.

Faster model loading: Smaller weights reduce model loading time, which is especially useful for mobile and edge deployments.

Reduced memory footprint: On-device memory use is lower, which allows running larger models or multiple models concurrently.

**Why Quantize Activations?**

Runtime efficiency: Activations are the intermediate outputs of each layer computed during the forward pass. Lower-precision activations (e.g., int8 instead of float32) require less memory bandwidth and compute.

End-to-end low-precision execution: Quantizing both weights and activations enables optimized hardware kernels (e.g., int8 × int8 → int32) to be used throughout the network, maximizing speed and energy efficiency.

Better cache locality: Smaller activation tensors are more cache-friendly, leading to faster inference.

---

*Quantizing only the weights can reduce model size but won’t deliver full runtime acceleration. Quantizing both weights and activations is essential to fully unlock the benefits of quantized inference on CPUs, mobile chips, and specialized accelerators.*

### Types of Quantization

**Floating Point Quantization**

Floating-point quantization reduces the bit-width of real-valued tensors, typically from 32-bit (float32) to 16-bit (float16 or bfloat16). 

![alt text](image.png)

**Integer Quantization**

Integer quantization maps real-valued numbers to a discrete integer range using an affine transformation. This process enables efficient inference using low-precision arithmetic.

**Reference**

[Neural Network Quantization in PyTorch By Arik Poznanski](https://arikpoz.github.io/posts/2025-04-16-neural-network-quantization-in-pytorch/)