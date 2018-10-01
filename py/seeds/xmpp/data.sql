DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    source TEXT,
    url TEXT,
    time timestamp DATE DEFAULT (datetime('now', 'localtime')),
    PRIMARY KEY (source, url)
);
