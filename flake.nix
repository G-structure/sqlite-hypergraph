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
          ];

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
        };

        defaultPackage = self.packages.${system}.wasm;
      }
    );
}
