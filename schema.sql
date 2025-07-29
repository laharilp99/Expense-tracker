
DROP TABLE IF EXISTS totalbalance;

CREATE TABLE IF NOT EXISTS totalbalance (
    slno INTEGER PRIMARY KEY AUTOINCREMENT,
    totalbalance TEXT NOT NULL,
    entrydate TEXT DEFAULT (DATE('now'))
);
            
            INSERT INTO totalbalance(totalbalance) values (100000);
