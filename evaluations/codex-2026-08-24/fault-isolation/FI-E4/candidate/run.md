# Run record

- Case: `FI-E4`
- Condition: `candidate`
- Prompt: Does this version of the SQLite driver serialize concurrent writes on one connection, or do we need our own mutex? Prove it with a small experiment.
- Expected routing: `code-research`
- Loaded skills observed in Codex events: `code-research, fault-isolation, implement-ticket, plan`
- Agent-reported selection (not a native harness event): `none`
- Final response:

**Research status:** `Blocked` for a local runtime experiment; `Supported` by source inspection for `mattn/go-sqlite3`.

**Question and decision**
You asked whether the SQLite driver serializes concurrent writes on one connection, or whether you need your own mutex.

What this changes:
- If the driver already serializes access on a single connection, adding your own mutex is redundant for correctness.
- If it does not, concurrent `Exec`/`Tx` use on one connection can race and corrupt behavior.

**Evidence ledger**
- `E1`: `go` is not installed in this workspace, so I could not run a local proof-of-behavior program. `go version` failed with `go: command not found`.
- `E2`: Go’s `database/sql.DB` is safe for concurrent use and manages a pool of connections, while per-connection state is only reliably observed on a `Conn` or `Tx`. See [`database/sql` docs](https://pkg.go.dev/database/sql) and the `DB`/`Conn` notes.
- `E3`: In [`mattn/go-sqlite3/sqlite3.go`](https://github.com/mattn/go-sqlite3/blob/master/sqlite3.go), `SQLiteConn` contains `mu sync.Mutex`, and `SQLiteStmt` also contains `mu sync.Mutex`.
- `E4`: The same driver opens SQLite with `SQLITE_OPEN_FULLMUTEX` by default before calling `sqlite3_open_v2(...)`, which requests serialized SQLite mutex mode. See [`sqlite3.go`](https://github.com/mattn/go-sqlite3/blob/master/sqlite3.go).
- `E5`: The README documents the `_mutex` DSN option with values `no` and `full`, implying mutex mode is an explicit connection-level setting. See [`README.md`](https://github.com/mattn/go-sqlite3/blob/master/README.md).

**Conclusion**
For `mattn/go-sqlite3`, concurrent operations on the same underlying connection are already serialized by the driver and SQLite’s full-mutex mode. You generally do **not** need your own mutex just to protect one `*sql.Conn`/transaction from concurrent goroutines.

Caveat: that is about **one connection**. It does **not** change SQLite’s own limitation that multiple connections still contend on writes at the database-file level.

**What I could not prove locally**
I could not run the small experiment in this container because the Go toolchain is unavailable. So the conclusion is source-backed, not runtime-verified here.

**If you want a runnable proof**
I can give you a tiny Go program that:
- starts two goroutines writing through the same `*sql.Conn`,
- records overlap timestamps,
- and shows whether the driver/connection serializes them.

If you tell me which driver you are actually using (`mattn/go-sqlite3`, `modernc.org/sqlite`, `glebarez/sqlite`, etc.), I’ll tailor the experiment to that exact driver.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
