DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    type TEXT,
    source TEXT,
    url TEXT,
    time timestamp DATE DEFAULT (datetime('now', 'localtime')),
    PRIMARY KEY (type, source, url)
);
