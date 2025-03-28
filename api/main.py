from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="user",
        password="pass",
        database="db_alan_marinho",
        port=3390,
    )


@app.route("/search_operadora", methods=["GET"])
def search_operadora():
    conn = None
    cursor = None
    try:

        search_term = request.args.get("rs", "")

        if not search_term:
            print("err")
            return jsonify({"error": "Termo de busca ausente"}), 400

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        query = """
          SELECT * FROM operadoras_de_plano_de_saude_ativas
          WHERE Razao_Social LIKE %s
          """
        cursor.execute(query, (f"%{search_term}%",))

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(result), 200
    except Exception as e:
        print(f"erro {e}")
        return jsonify({"error": "Ocorreu um erro"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route("/", methods=["GET"])
def index():
    return jsonify({"Projeto": "Testes de livelamento", "candidato": "Alan Marinho"})


if __name__ == "__main__":
    app.run(debug=True)
