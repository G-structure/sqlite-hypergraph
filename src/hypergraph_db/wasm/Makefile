# src/hypergraph_db/wasm/Makefile
DIST_DIR=dist
WASM_DIR=$(DIST_DIR)/.wasm

$(DIST_DIR):
	mkdir -p $(DIST_DIR)

$(WASM_DIR): $(DIST_DIR)
	mkdir -p $(WASM_DIR)

TARGET_WASM=$(WASM_DIR)/hypergraph.js
TARGET_WASM_WASM=$(WASM_DIR)/hypergraph.wasm

SQLITE_VEC_DIR=$(SQLITE_VEC_SRC)
SQLITE_LEMBED_DIR=$(SQLITE_LEMBED_SRC)

# Download SQLite amalgamation if needed
SQLITE_AMALGAMATION=sqlite-amalgamation-3450100
SQLITE_DOWNLOAD_URL=https://www.sqlite.org/2024/$(SQLITE_AMALGAMATION).zip

$(DIST_DIR)/$(SQLITE_AMALGAMATION):
	curl -o $(DIST_DIR)/sqlite.zip $(SQLITE_DOWNLOAD_URL)
	cd $(DIST_DIR) && unzip sqlite.zip
	rm $(DIST_DIR)/sqlite.zip

$(TARGET_WASM): hypergraph.c $(WASM_DIR) $(DIST_DIR)/$(SQLITE_AMALGAMATION)
	emcc -O3 \
		-I. \
		-I$(SQLITE_VEC_DIR) \
		-I$(SQLITE_LEMBED_DIR) \
		-I$(DIST_DIR)/$(SQLITE_AMALGAMATION) \
		$(DIST_DIR)/$(SQLITE_AMALGAMATION)/sqlite3.c \
		-s WASM=1 \
		-s EXPORTED_FUNCTIONS='["_malloc", "_free", "_init_hypergraph_db", "_insert_node"]' \
		-s EXPORTED_RUNTIME_METHODS='["ccall", "cwrap", "stringToUTF8", "UTF8ToString"]' \
		-s ALLOW_MEMORY_GROWTH=1 \
		-s USE_SQLITE3=1 \
		-o $@ \
		$<

wasm: $(TARGET_WASM)

.PHONY: wasm clean

clean:
	rm -rf $(DIST_DIR)
