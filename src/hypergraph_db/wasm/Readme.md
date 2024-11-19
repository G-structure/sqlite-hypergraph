# Hypergraph DB WASM Build Guide

This document explains how to build the WebAssembly (WASM) version of Hypergraph DB, which includes SQLite and the required extensions (sqlite-vec and sqlite-lembed).

## Prerequisites

You need to have Nix installed with flakes enabled. If you haven't already, install Nix:

1. Install Nix:
```bash
curl -L https://nixos.org/nix/install | sh
```

2. Enable flakes by creating or editing `~/.config/nix/nix.conf`:
```
experimental-features = nix-command flakes
```

## Building

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sqlite-hypergraph.git
cd sqlite-hypergraph
```

2. Build the WASM target:
```bash
nix build .#wasm
```

The build outputs will be in `result/`, containing:
- `hypergraph.js` - JavaScript glue code
- `hypergraph.wasm` - WebAssembly binary

## Development

For development, you can use the dev shell which provides all necessary tools:

```bash
nix develop
```

This gives you access to:
- emscripten
- gcc
- make
- python3
- sqlite

### Manual Build

If you want to build manually (outside of Nix):

1. Make sure you have emscripten installed:
```bash
git clone https://github.com/emscripten-core/emsdk.git
cd emsdk
./emsdk install latest
./emsdk activate latest
source ./emsdk_env.sh
```

2. Navigate to the WASM source directory:
```bash
cd src/hypergraph_db/wasm
```

3. Build:
```bash
make
```

## Project Structure

```
sqlite-hypergraph/
├── flake.nix                # Nix build configuration
└── src/
    └── hypergraph_db/
        └── wasm/
            ├── Makefile     # WASM build rules
            └── hypergraph.c # Main WASM interface code
```

## Details

The WASM build:
- Compiles SQLite from source
- Integrates sqlite-vec for vector operations
- Integrates sqlite-lembed for embeddings
- Exposes a JavaScript API for interfacing with the hypergraph database

### Build Components

The build process combines several components:
- SQLite amalgamation source
- sqlite-vec extension
- sqlite-lembed extension
- Hypergraph DB interface code

These are compiled together into a single WASM module with the necessary JavaScript bindings.

### Exported Functions

The WASM build exports these main functions:
- `init_hypergraph_db` - Initialize the database
- `insert_node` - Insert a node into the graph
- (additional functions as needed)

## Using the Built WASM

After building, you can use the WASM module in a web application:

```javascript
// Initialize the module
const hypergraph = await HypergraphDB.init();

// Create a new database
await hypergraph.init_hypergraph_db("mydatabase.db");

// Insert a node
const node = {
  id: "node1",
  data: "Some data"
};
await hypergraph.insertNode(node);
```

## Troubleshooting

Common issues and solutions:

1. **Build fails with emscripten cache errors**
   - Make sure TMPDIR is writable
   - Clear emscripten cache: `emcc --clear-cache`

2. **Missing dependencies**
   - Run `nix develop` to ensure all dependencies are available
   - Check that all required extensions are present in build directory

3. **WASM file not generated**
   - Check emcc output for detailed error messages
   - Verify that all source files are present in build directory

## License

This project is licensed under the MIT License - see the LICENSE file for details.
