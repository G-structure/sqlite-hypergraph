# Download the embedding model and place it in the correct folder
download-model:
    @echo "Creating ./src/hypergraph_db/sql/models directory if it doesn't exist..."
    mkdir -p src/hypergraph_db/sql/models
    @echo "Downloading the all-MiniLM-L6-v2 model..."
    curl -L -o src/hypergraph_db/sql/models/all-MiniLM-L6-v2.e4ce9877.q8_0.gguf https://huggingface.co/asg017/sqlite-lembed-model-examples/resolve/main/all-MiniLM-L6-v2/all-MiniLM-L6-v2.e4ce9877.q8_0.gguf
    @echo "Download complete. Model saved to ./src/hypergraph_db/sql/models/all-MiniLM-L6-v2.e4ce9877.q8_0.gguf."

# Download and install sqlite-lembed extension
install-sqlite-lembed:
    @echo "Creating ./src/hypergraph_db/sql directory if it doesn't exist..."
    mkdir -p src/hypergraph_db/sql
    @echo "Downloading and installing sqlite-lembed extension..."
    curl -L -o install.sh https://github.com/asg017/sqlite-lembed/releases/download/v0.0.1-alpha.8/install.sh
    chmod +x install.sh
    ./install.sh loadable --prefix=src/hypergraph_db/sql
    rm install.sh
    @echo "sqlite-lembed has been successfully installed in ./src/hypergraph_db/sql."

# Download and install sqlite-vec extension
install-sqlite-vec:
    @echo "Creating ./src/hypergraph_db/sql directory if it doesn't exist..."
    mkdir -p src/hypergraph_db/sql
    @echo "Downloading and installing sqlite-vec extension..."
    curl -L -o install.sh https://github.com/asg017/sqlite-vec/releases/download/v0.1.3/install.sh
    chmod +x install.sh
    ./install.sh loadable --prefix=src/hypergraph_db/sql
    rm install.sh
    @echo "sqlite-vec has been successfully installed in ./src/hypergraph_db/sql."

# Run all commands in sequence
play: download-model install-sqlite-lembed install-sqlite-vec
    @echo "All commands executed successfully."