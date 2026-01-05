CREATE TABLE IF NOT EXISTS mariadb_logs (
    id SERIAL PRIMARY KEY,
    log_type VARCHAR(50),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE mariadb_logs TO app_user;

GRANT USAGE, SELECT ON SEQUENCE mariadb_logs_id_seq TO app_user;

