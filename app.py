from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

DB_PATH = Path("catalago.db")

app = Flask(__name__)
app.secret_key = "dev-key-please-change"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Se o banco já existe, não faz nada
    if DB_PATH.exists():
        return

    schema_path = Path("schema.sql")
    if not schema_path.exists():
        raise FileNotFoundError("Arquivo schema.sql não encontrado na mesma pasta do app.py")

    with get_conn() as conn:
        conn.executescript(schema_path.read_text(encoding="utf-8"))

        # Dados iniciais
        conn.execute(
            "INSERT INTO cursos (titulo, descricao, categoria, carga_horaria) VALUES (?, ?, ?, ?)",
            ("Introdução à lógica de programação", "Conceitos básicos de lógica e algoritmos.", "Computação", 60),
        )
        conn.execute(
            "INSERT INTO cursos (titulo, descricao, categoria, carga_horaria) VALUES (?, ?, ?, ?)",
            ("Didática", "Fundamentos do ensino e aprendizagem.", "Educação", 40),
        )
        conn.commit()


# ✅ Flask 3: inicializa o banco ao subir a aplicação (substitui before_first_request)
with app.app_context():
    init_db()


@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q", "").strip()

    with get_conn() as conn:
        if q:
            cursos = conn.execute(
                "SELECT * FROM cursos WHERE titulo LIKE ? OR categoria LIKE ? ORDER BY id DESC",
                (f"%{q}%", f"%{q}%"),
            ).fetchall()
        else:
            cursos = conn.execute("SELECT * FROM cursos ORDER BY id DESC").fetchall()

    return render_template("index.html", cursos=cursos, q=q)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    with get_conn() as conn:
        if request.method == "POST":
            curso_id = (request.form.get("id") or "").strip()

            titulo = (request.form.get("titulo") or "").strip()
            descricao = (request.form.get("descricao") or "").strip()
            categoria = (request.form.get("categoria") or "").strip()
            carga_horaria = (request.form.get("carga_horaria") or "").strip()

            if not titulo:
                flash("Título é obrigatório.", "error")
                return redirect(url_for("admin"))

            try:
                ch_int = int(carga_horaria) if carga_horaria else 0
            except ValueError:
                flash("Carga horária deve ser um número inteiro.", "error")
                return redirect(url_for("admin"))

            if curso_id:
                conn.execute(
                    "UPDATE cursos SET titulo=?, descricao=?, categoria=?, carga_horaria=? WHERE id=?",
                    (titulo, descricao, categoria, ch_int, curso_id),
                )
                flash("Curso atualizado com sucesso!", "success")
            else:
                conn.execute(
                    "INSERT INTO cursos (titulo, descricao, categoria, carga_horaria) VALUES (?, ?, ?, ?)",
                    (titulo, descricao, categoria, ch_int),
                )
                flash("Curso cadastrado com sucesso!", "success")

            conn.commit()
            return redirect(url_for("admin"))

        cursos = conn.execute("SELECT * FROM cursos ORDER BY id DESC").fetchall()

    return render_template("admin.html", cursos=cursos)


@app.route("/delete/<int:curso_id>", methods=["POST"])
def delete(curso_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM cursos WHERE id=?", (curso_id,))
        conn.commit()

    flash("Curso excluído!", "success")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
