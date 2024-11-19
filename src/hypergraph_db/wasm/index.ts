declare var Module: any;

export class HypergraphDB {
  private db: any;
  private dbPath: string;

  constructor(dbPath: string) {
    this.dbPath = dbPath;
  }

  async initialize(): Promise<void> {
    // Wait for WASM module to load
    await Module.ready;

    // Create cwrap functions
    this.db = {
      init: Module.cwrap("init_hypergraph_db", "number", ["string"]),
      insertNode: Module.cwrap("insert_node", "number", ["string", "string"]),
    };

    // Initialize database
    const result = this.db.init(this.dbPath);
    if (result !== 0) {
      throw new Error(`Failed to initialize database: ${result}`);
    }
  }

  async insertNode(body: object): Promise<void> {
    const jsonBody = JSON.stringify(body);
    const result = this.db.insertNode(this.dbPath, jsonBody);
    if (result !== 0) {
      throw new Error(`Failed to insert node: ${result}`);
    }
  }
}
