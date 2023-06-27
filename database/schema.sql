DROP TABLE IF EXISTS akce;

CREATE TABLE akce (
    id_akce            INTEGER PRIMARY KEY AUTOINCREMENT,
    jmeno              TEXT NOT NULL,
    datum              TEXT NOT NULL,
    misto              TEXT NOT NULL,
    zacatek_akce       TEXT NOT NULL,
    konec_akce         TEXT NOT NULL,
    popis              TEXT,
    program_id_program INTEGER,
    je_public          BOOL NOT NULL,
    FOREIGN KEY (program_id_program) REFERENCES program(id_program)
);

DROP TABLE IF EXISTS dochazka;

CREATE TABLE dochazka (
    dochazka     BOOL NOT NULL,
    duvod        TEXT,
    user_id_user INTEGER,
    akce_id_akce INTEGER,
    FOREIGN KEY (user_id_user) REFERENCES user(id_user),
    FOREIGN KEY (akce_id_akce) REFERENCES akce(id_akce),
    PRIMARY KEY (user_id_user, akce_id_akce)
);

DROP TABLE IF EXISTS druzina;

CREATE TABLE druzina (
    id_druzina    INTEGER PRIMARY KEY AUTOINCREMENT,
    jmeno         TEXT NOT NULL,
    nejmladsi_vek INTEGER NOT NULL,
    popis         TEXT
);

DROP TABLE IF EXISTS druzina_akce;

CREATE TABLE druzina_akce (
    akce_id_akce       INTEGER,
    druzina_id_druzina INTEGER,
    FOREIGN KEY (druzina_id_druzina) REFERENCES druzina (id_druzina),
    FOREIGN KEY (akce_id_akce) REFERENCES akce (id_akce),
    PRIMARY KEY (akce_id_akce, druzina_id_druzina)
);

DROP TABLE IF EXISTS program;

CREATE TABLE program (
    id_program     INTEGER PRIMARY KEY AUTOINCREMENT ,
    misto_program          TEXT NOT NULL,
    popis_program          TEXT NOT NULL,
    delka          TEXT NOT NULL,
    doporuceny_vek INTEGER
);

DROP TABLE IF EXISTS role;

CREATE TABLE role (
    id_role INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev   TEXT NOT NULL
);

DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id_user             INTEGER PRIMARY KEY AUTOINCREMENT,
    login               TEXT NOT NULL,
    heslo               TEXT NOT NULL,
    rodne_cislo         TEXT NOT NULL,
    jmeno               TEXT NOT NULL,
    prijmeni            TEXT NOT NULL,
    adresa              TEXT NOT NULL,
    telefon             INTEGER NOT NULL,
    email               TEXT NOT NULL,
    datum_narozeni      TEXT NOT NULL,
    je_aktivni          INTEGER,
    id_rodice           INTEGER,
    role_id_role        INTEGER NOT NULL,
    id_druzina_vede     INTEGER,
    id_druzina_clenem     INTEGER,
    FOREIGN KEY (id_rodice) REFERENCES user(id_user),
    FOREIGN KEY (id_druzina_vede) REFERENCES druzina(id_druzina),
    FOREIGN KEY (id_druzina_clenem) REFERENCES druzina(id_druzina),
    FOREIGN KEY (role_id_role) REFERENCES role(id_role)
);

DROP TABLE IF EXISTS user_akce;

CREATE TABLE user_akce (
    user_id_user INTEGER,
    akce_id_akce INTEGER,
    FOREIGN KEY (user_id_user) REFERENCES user (id_user),
    FOREIGN KEY (akce_id_akce) REFERENCES akce (id_akce),
    PRIMARY KEY (user_id_user, akce_id_akce)
);

-- Inserting data
INSERT INTO akce (jmeno, datum, misto, zacatek_akce, konec_akce, popis, program_id_program, je_public) VALUES('Tabor', '01.02.2023', 'PEF Mendelu', '29.01.2023', '03.02.2023', 'super', 1, 1);
INSERT INTO akce (jmeno, datum, misto, zacatek_akce, konec_akce, popis, program_id_program, je_public) VALUES('Vychazka', '29.07.2023', 'Brno', '27.07.2023', '01.08.2023', 'super', 1, 1);
INSERT INTO akce (jmeno, datum, misto, zacatek_akce, konec_akce, popis, program_id_program, je_public) VALUES('Vychazka', '29.09.2023', 'Brno', '27.09.2023', '10.10.2023', 'super super', 1, 0);

INSERT INTO program (misto_program, popis_program, delka, doporuceny_vek) VALUES ('les', 'pecka program', 'hodina', 12);

INSERT INTO role (nazev) VALUES ('administrator');
INSERT INTO role (nazev) VALUES ('vedouci');
INSERT INTO role (nazev) VALUES ('rodic');
INSERT INTO role (nazev) VALUES ('dite');

INSERT INTO user (login, heslo, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni, role_id_role) VALUES ('xnavra18', '55863a2db485cd281fa934bfff935bb3f689dd8775d3b9f3df95456867c02966', 00, 'Martin', 'Navratil', 'Blansko', 420000000000, 'email1@project.cz', '1.1.2022', 1);
INSERT INTO user (login, heslo, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni, role_id_role) VALUES ('daniljepan', '55863a2db485cd281fa934bfff935bb3f689dd8775d3b9f3df95456867c02966', 00, 'Daniil', 'Astapenko', 'Brno', 420000000001, 'email2@project.cz', '1.1.2022', 2);
INSERT INTO user (login, heslo, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni, role_id_role) VALUES ('filipjede', '55863a2db485cd281fa934bfff935bb3f689dd8775d3b9f3df95456867c02966', 00, 'Filip', 'Adamek', 'Brno', 420000000003, 'email3@project.cz', '1.1.2022', 3);
INSERT INTO user (login, heslo, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni, role_id_role) VALUES ('filipjede1', '55863a2db485cd281fa934bfff935bb3f689dd8775d3b9f3df95456867c02966', 00, 'Nerodic', 'Test', 'Brno', 420000000003, 'email3@project.cz', '1.1.2022', 3);
INSERT INTO user (login, heslo, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni, role_id_role) VALUES ('frajerpavol', '55863a2db485cd281fa934bfff935bb3f689dd8775d3b9f3df95456867c02966', 00, 'Pavol', 'Fasko', 'Brno', 420000000004, 'email4@project.cz', '1.1.2022', 4);
INSERT INTO user (login, heslo, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni, id_rodice, role_id_role) VALUES ('testdite1', '55863a2db485cd281fa934bfff935bb3f689dd8775d3b9f3df95456867c02966', 00, 'Anicka', 'Adamkova', 'Brno', 420, 'anicka.07@seznam.cz', '1.1.2022', 3, 4);
INSERT INTO user (login, heslo, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni, id_rodice, role_id_role) VALUES ('testdite2', '55863a2db485cd281fa934bfff935bb3f689dd8775d3b9f3df95456867c02966', 00, 'Manicka', 'Adamkova', 'Brno', 420, 'manicka@seznam.cz', '1.1.2022', 3, 4);
INSERT INTO user (login, heslo, rodne_cislo, jmeno, prijmeni, adresa, telefon, email, datum_narozeni, id_rodice, role_id_role) VALUES ('testdite3', '55863a2db485cd281fa934bfff935bb3f689dd8775d3b9f3df95456867c02966', 00, 'Janicka', 'Adamkova', 'Brno', 420, 'janicka08@seznam.cz', '1.1.2022', 3, 4);

INSERT INTO druzina(jmeno, nejmladsi_vek, popis) VALUES ('Želvičky', 8, 'druzina mladsich holek');
INSERT INTO druzina(jmeno, nejmladsi_vek, popis) VALUES ('Tygři', 12, 'druzina starsich kluku');

