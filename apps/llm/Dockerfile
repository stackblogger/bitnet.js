FROM python:3.9-alpine

# Install necessary dependencies and tools
RUN apk add --no-cache build-base cmake clang git && \
    rm -rf /var/cache/apk/*

# Clone the BitNet repository without history
RUN git clone --recursive --depth 1 https://github.com/microsoft/BitNet.git && \
    rm -rf BitNet/.git

WORKDIR /BitNet

# Install Python dependencies
RUN pip install -r requirements.txt && \
    pip cache purge

# Copy the local requirements.txt for additional dependencies
COPY requirements-local.txt .

# Install additional dependencies from the local requirements file
RUN pip install -r requirements-local.txt && \
    pip cache purge

# Run the code generation for Llama3-8B model
RUN python3 utils/codegen_tl2.py --model Llama3-8B-1.58-100B-tokens --BM 256,128,256,128 --BK 96,96,96,96 --bm 32,32,32,32

# Build the model using cmake with specified compilers
RUN cmake -B build -DBITNET_X86_TL2=ON -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ && \
    cmake --build build --target llama-cli --config Release

# Download the Llama model from HuggingFace
ADD https://huggingface.co/brunopio/Llama3-8B-1.58-100B-tokens-GGUF/resolve/main/Llama3-8B-1.58-100B-tokens-TQ2_0.gguf .

# Verify the integrity of the model file
RUN echo "2565559c82a1d03ecd1101f536c5e99418d07e55a88bd5e391ed734f6b3989ac Llama3-8B-1.58-100B-tokens-TQ2_0.gguf" | sha256sum -c

# Expose port for communication with the Node.js app
EXPOSE 5000

# Run a Python script that handles queries from the Node.js app using socket.io
COPY run_model.py .

# Run the model in inference mode, listening for queries
CMD ["python3", "run_model.py", "-m", "Llama3-8B-1.58-100B-tokens-TQ2_0.gguf"]
