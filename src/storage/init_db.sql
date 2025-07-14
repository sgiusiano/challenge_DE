-- Drop existing tables
DROP TABLE IF EXISTS challenge.raw.events;
DROP TABLE IF EXISTS challenge.trusted.events;
DROP TABLE IF EXISTS challenge.trusted.documents;
DROP TABLE IF EXISTS challenge.trusted.users;
DROP TABLE IF EXISTS challenge.marts.sessions;

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS trusted;
CREATE SCHEMA IF NOT EXISTS marts;
-- Create RAW events table
CREATE TABLE IF NOT EXISTS challenge.raw.events
(
    event_id VARCHAR(100) NOT NULL,
    "timestamp" timestamp NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    document_id VARCHAR(100) NOT NULL,
    comment_text VARCHAR(100),
    edit_length VARCHAR(100),
    shared_with VARCHAR(100),
    _source_file VARCHAR(100),
    _ingested_at timestamp NOT NULL
);

-- Create users table
CREATE TABLE challenge.trusted.users (
    user_id VARCHAR(100) PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    days_from_last_activity INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create documents table
CREATE TABLE challenge.trusted.documents (
    document_id VARCHAR(100) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    last_modified TIMESTAMP NOT NULL,
    document_word_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    shared_with_count INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create events table
CREATE TABLE challenge.trusted.events (
    event_id VARCHAR(100) PRIMARY KEY,
    "timestamp" TIMESTAMP NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) REFERENCES challenge.trusted.users(user_id),
    document_id VARCHAR(100) REFERENCES challenge.trusted.documents(document_id),
    comment_text VARCHAR(100),
    edit_length INTEGER,
    shared_with VARCHAR(100),
    _source_file VARCHAR(100),
    _ingested_at TIMESTAMP NOT NULL,
    day_of_week VARCHAR(10),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE  challenge.marts.sessions
(
    event_id VARCHAR(100),
    user_id VARCHAR(100),
    "timestamp" timestamp without time zone,
    next_interaction timestamp,
    minutes_transcurred double precision,
    session_duration double precision
);
