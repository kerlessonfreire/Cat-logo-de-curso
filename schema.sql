DROP TABLE IF EXISTS cursos;

CREATE TABLE IF NOT EXISTS cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    categoria TEXT,
    carga_horaria INTEGER
);
