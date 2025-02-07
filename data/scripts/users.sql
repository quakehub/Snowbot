CREATE TABLE IF NOT EXISTS useravatars (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    avatar_id BIGINT,
    insertion TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);
CREATE INDEX IF NOT EXISTS useravatars_idx ON useravatars(user_id, avatar_id);

CREATE TABLE IF NOT EXISTS useravatars (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    avatar_id BIGINT,
    insertion TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);
CREATE INDEX IF NOT EXISTS useravatars_idx ON useravatars(user_id, avatar_id);

CREATE TABLE IF NOT EXISTS usernames (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    username TEXT,
    insertion TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);
CREATE INDEX IF NOT EXISTS usernames_idx ON usernames(user_id, username);


CREATE TABLE IF NOT EXISTS usernicks (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT,
    server_id BIGINT,
    nickname TEXT,
    insertion TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);
CREATE INDEX IF NOT EXISTS usernicks_idx ON usernicks(user_id, nickname);


CREATE TABLE IF NOT EXISTS userroles (
    user_id BIGINT,
    server_id BIGINT,
    roles TEXT,
    UNIQUE(user_id, server_id)
);

CREATE TABLE IF NOT EXISTS usertime (
    user_id BIGINT PRIMARY KEY,
    timezone VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS tracker (
    user_id BIGINT PRIMARY KEY,
    unix NUMERIC,
    action TEXT
);

CREATE TABLE IF NOT EXISTS userstatus (
    user_id BIGINT PRIMARY KEY,
    online DOUBLE PRECISION DEFAULT 0 NOT NULL,
    idle DOUBLE PRECISION DEFAULT 0 NOT NULL,
    dnd DOUBLE PRECISION DEFAULT 0 NOT NULL,
    last_changed DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW()),
    starttime DOUBLE PRECISION DEFAULT EXTRACT(EPOCH FROM NOW())
);