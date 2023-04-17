create table if not exists "Article" (
    id integer primary key autoincrement,
    url text,
    "desc" text,
    file text
);


create unique index if not exists art_idx on "Article"(url, "desc", file);