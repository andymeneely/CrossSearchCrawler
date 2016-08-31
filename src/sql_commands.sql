CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY,
    name text
);

CREATE TABLE IF NOT EXISTS publications (
    id INTEGER PRIMARY KEY,
    title text,
    year text,
    doi text,
    isbn text,
    issn text,
    url text,
    startpage text,
    endpage text
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    name text
);

CREATE TABLE IF NOT EXISTS authorpublink (
    authorID INTEGER,
    pubID INTEGER
);

CREATE TABLE IF NOT EXISTS tagpublink (
    tagID INTEGER,
    pubID INTEGER
);

CREATE TABLE IF NOT EXISTS searches (
    id INTEGER PRIMARY KEY,
    metric text,
    searchText text,
    site text
);

CREATE TABLE IF NOT EXISTS searchpublink (
    searchID INTEGER,
    pubID INTEGER
);

CREATE INDEX IF NOT EXISTS searchIDIndex ON searches(id);
CREATE INDEX IF NOT EXISTS searchTextIndex ON searches(searchText);
CREATE INDEX IF NOT EXISTS searchSiteIndex ON searches(site);

CREATE INDEX IF NOT EXISTS SPLsIDIndex ON searchpublink(searchID);
CREATE INDEX IF NOT EXISTS SPLpIDIndex ON searchpublink(pubID);

CREATE INDEX IF NOT EXISTS pubIDIndex ON publications(id);
CREATE INDEX IF NOT EXISTS pubTitleIndex ON publications(title);
CREATE INDEX IF NOT EXISTS pubYearIndex ON publications(year);
CREATE INDEX IF NOT EXISTS pubDOIIndex ON publications(doi);
CREATE INDEX IF NOT EXISTS pubISBNIndex ON publications(isbn);
CREATE INDEX IF NOT EXISTS pubISSNIndex ON publications(issn);

CREATE INDEX IF NOT EXISTS APLaIDIndex ON authorpublink(authorID);
CREATE INDEX IF NOT EXISTS APLpIDIndex ON authorpublink(pubID);

CREATE INDEX IF NOT EXISTS authorIDIndex ON authors(id);
CREATE INDEX IF NOT EXISTS authorNameIndex ON authors(name);

