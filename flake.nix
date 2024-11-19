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
            gcc
            gnumake
            python3
            sqlite
            curl
          ];

          shellHook = ''
            export SQLITE_VEC_SRC=${sqlite-vec}
            export SQLITE_LEMBED_SRC=${sqlite-lembed}
            source ${pkgs.emscripten}/share/emscripten/env
          '';
        };

        packages.wasm = pkgs.stdenv.mkDerivation {
          pname = "hypergraph-wasm";
          version = "0.1.0";

          src = ./src/hypergraph_db/wasm;

          nativeBuildInputs = with pkgs; [
            emscripten
            gcc
            gnumake
            python3
            sqlite
            curl
          ];

          # Create temp directories for Emscripten
          preBuild = ''
            # Create cache directories
            export EM_CACHE=$TMPDIR/emscripten/cache
            export EM_PORTS=$TMPDIR/emscripten/ports
            mkdir -p $EM_CACHE $EM_PORTS

            # Source emscripten environment
            source ${pkgs.emscripten}/share/emscripten/env
          '';

          buildPhase = ''
            # Set environment variables
            export SQLITE_VEC_SRC=${sqlite-vec}
            export SQLITE_LEMBED_SRC=${sqlite-lembed}

            # Create output directories
            mkdir -p dist/.wasm

            # Build using our Makefile
            make wasm
          '';

          installPhase = ''
            mkdir -p $out
            cp dist/.wasm/* $out/
          '';

          # Use TMPDIR for temporary files
          TMPDIR = "/tmp";
        };

        defaultPackage = self.packages.${system}.wasm;
      }
    );
}
