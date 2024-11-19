#include <emscripten.h>
#include <sqlite3.h>
#include "sqlite-vec.h"
#include "sqlite-lembed.h"

EMSCRIPTEN_KEEPALIVE
int init_hypergraph_db(const char* db_path) {
    sqlite3* db;
    int rc = sqlite3_open(db_path, &db);
    if (rc != SQLITE_OK) {
        return rc;
    }

    // Load extensions
    rc = sqlite3_load_extension(db, "vec0", "sqlite3_vec_init", 0);
    if (rc != SQLITE_OK) {
        sqlite3_close(db);
        return rc;
    }

    rc = sqlite3_load_extension(db, "lembed0", "sqlite3_lembed_init", 0);
    if (rc != SQLITE_OK) {
        sqlite3_close(db);
        return rc;
    }

    // Initialize schema
    const char* schema_sql =
        "CREATE TABLE IF NOT EXISTS nodes ("
        "  body TEXT,"
        "  id TEXT GENERATED ALWAYS AS (json_extract(body, '$.id')) VIRTUAL NOT NULL UNIQUE,"
        "  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP"
        ");"

        "CREATE TABLE IF NOT EXISTS hyperedges ("
        "  id TEXT PRIMARY KEY,"
        "  properties TEXT,"
        "  nodes TEXT,"
        "  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP"
        ");"

        "CREATE TABLE IF NOT EXISTS node_hyperedge_map ("
        "  hyperedge_id TEXT,"
        "  node_id TEXT,"
        "  node_order INTEGER,"
        "  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "  FOREIGN KEY(hyperedge_id) REFERENCES hyperedges(id),"
        "  FOREIGN KEY(node_id) REFERENCES nodes(id)"
        ");"

        "CREATE VIRTUAL TABLE IF NOT EXISTS embeddings USING vec0("
        "  embedding float[384]"
        ");";

    char* err_msg = 0;
    rc = sqlite3_exec(db, schema_sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        sqlite3_free(err_msg);
        sqlite3_close(db);
        return rc;
    }

    sqlite3_close(db);
    return SQLITE_OK;
}

EMSCRIPTEN_KEEPALIVE
int insert_node(const char* db_path, const char* body) {
    sqlite3* db;
    int rc = sqlite3_open(db_path, &db);
    if (rc != SQLITE_OK) {
        return rc;
    }

    const char* sql = "INSERT INTO nodes (body) VALUES (json(?))";
    sqlite3_stmt* stmt;
    rc = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
    if (rc != SQLITE_OK) {
        sqlite3_close(db);
        return rc;
    }

    sqlite3_bind_text(stmt, 1, body, -1, SQLITE_STATIC);
    rc = sqlite3_step(stmt);

    sqlite3_finalize(stmt);
    sqlite3_close(db);

    return rc == SQLITE_DONE ? SQLITE_OK : rc;
}
