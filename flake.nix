{
  description = "Hypergraph DB WASM build";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";

    sqlite-vec = {
      url = "github:asg017/sqlite-vec";
      flake = false;
    };

    sqlite-lembed = {
      url = "github:asg017/sqlite-lembed";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, flake-utils, sqlite-vec, sqlite-lembed }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            emscripten
            cmake
            gcc
            gnumake
            python3
            sqlite
          ];

          shellHook = ''
            # Set up build environment
            export SQLITE_VEC_SRC=${sqlite-vec}
            export SQLITE_LEMBED_SRC=${sqlite-lembed}

            # Configure emscripten
            source ${pkgs.emscripten}/share/emscripten/env
          '';
        };

        packages.wasm = pkgs.stdenv.mkDerivation {
          pname = "hypergraph-wasm";
          version = "0.1.0";

          src = ./.;

          nativeBuildInputs = with pkgs; [
            emscripten
            cmake
            gcc
            gnumake
            python3
            sqlite
          ];

          buildPhase = ''
            # Create build directories
            mkdir -p dist/.wasm

            # Build sqlite-vec WASM
            cp -r $SQLITE_VEC_SRC/* .
            emmake make wasm

            # Build sqlite-lembed WASM
            cp -r $SQLITE_LEMBED_SRC/* .
            emmake make wasm

            # Build our hypergraph WASM module
            emcc -O3 \
              -I. \
              -I$SQLITE_VEC_SRC \
              -I$SQLITE_LEMBED_SRC \
              -s WASM=1 \
              -s EXPORTED_FUNCTIONS='["_malloc", "_free", "_init_hypergraph_db", "_insert_node"]' \
              -s EXPORTED_RUNTIME_METHODS='["ccall", "cwrap", "stringToUTF8", "UTF8ToString"]' \
              -s ALLOW_MEMORY_GROWTH=1 \
              -o dist/.wasm/hypergraph.js \
              src/hypergraph_db/wasm/hypergraph.c
          '';

          installPhase = ''
            mkdir -p $out
            cp dist/.wasm/* $out/
          '';
        };

        defaultPackage = self.packages.${system}.wasm;
      }
    );
}
