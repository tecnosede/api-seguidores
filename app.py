from flask import Flask, request, jsonify
import instaloader

app = Flask(__name__)

def seguidores_instagram(usuario):
    loader = instaloader.Instaloader()
    perfil = instaloader.Profile.from_username(loader.context, usuario)
    return perfil.followers

@app.route('/seguidores', methods=['GET'])
def seguidores():
    usuario = request.args.get('usuario')
    if not usuario:
        return jsonify({"erro": "Informe o parametro usuario"}), 400
    try:
        total = seguidores_instagram(usuario)
        return jsonify({"usuario": usuario, "seguidores": total})
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500

@app.route('/')
def home():
    return "API funcionando!"

if __name__ == "__main__":
    app.run(debug=True)
