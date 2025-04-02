from flask import Flask, request, jsonify
import instaloader
from TikTokApi import TikTokApi

app = Flask(__name__)

# Consultar seguidores Instagram
def instagram_seguidores(usuario):
    loader = instaloader.Instaloader()
    perfil = instaloader.Profile.from_username(loader.context, usuario)
    return perfil.followers

# Consultar seguidores TikTok
def tiktok_seguidores(usuario):
    with TikTokApi() as api:
        user = api.user(username=usuario)
        info = user.info_full()
        return info['stats']['followerCount']

# Rota principal da API
@app.route('/seguidores', methods=['GET'])
def seguidores():
    usuario = request.args.get('usuario')
    rede = request.args.get('rede')

    if not usuario or not rede:
        return jsonify({"erro": "Informe os parâmetros usuario e rede"}), 400

    try:
        if rede.lower() == 'instagram':
            total = instagram_seguidores(usuario)
        elif rede.lower() == 'tiktok':
            total = tiktok_seguidores(usuario)
        else:
            return jsonify({"erro": "Rede inválida. Use 'instagram' ou 'tiktok'."}), 400

        return jsonify({"usuario": usuario, "rede": rede, "seguidores": total})

    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500

if __name__ == "__main__":
    app.run(debug=True)
