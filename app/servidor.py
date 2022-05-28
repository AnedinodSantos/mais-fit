from flask import Flask, request, jsonify
from flask_cors import CORS

from database import *
from helpers import retorna_idade


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Olá, você está na API da mais-fit!"


@app.route("/lista")
async def listar_sabores():
    try:
        data = await lista_sabores_ativos()
        return jsonify(data) , 200
    except Exception:
        return {"message": "Conexão perdida durante consulta ao banco"}, 503


@app.route("/kits")
async def listar_kits():
    try:
        kits = await lista_kits_ativos()
        return jsonify(kits), 200
    except Exception:
        return {"message": "Conexão perdida durante consulta ao banco"}, 503


@app.route("/formapagamento")
async def listar_pagamentos():
    try:
        pagamentos = await lista_pagamentos_ativo()
        return jsonify(pagamentos)
    except Exception:
        return {"message": "Conexão perdida durante consulta ao banco"}, 503


@app.route("/clientes", methods=['POST'])
async def cadastra_cliente():
    dados_cliente = request.json

    idade = retorna_idade(dados_cliente['nascimento'])
    cpf_exists = await cpf_existe(dados_cliente['cpf'])
    email_exists = await email_existe(dados_cliente['email'])

    if cpf_exists:
        return {"message": "Ja existe um cliente com esse CPF"}, 400
    if idade < 10:
        return {"message": "Este cliente possui idade menor que 10 anos"}, 400
    if email_exists:
        return {"message": "Ja existe um cliente com esse e-mail"}, 400

    try:
        await cadastrar_cliente(dados_cliente)
    except:
        return {"message": "Nao foi possivel cadastrar o cliente."}, 500

    return {"message": "Cliente cadastrado com sucesso!"}, 200


@app.route("/clientes", methods=['GET'])
async def listar_cliente():
    try:
        clientes = await listar_clientes()
        return jsonify(clientes), 200
    except Exception:
        return {"message": "Conexão perdida durante consulta ao banco"}, 503


@app.route("/verifica-cpf/<cpf>")
async def verifica_cpf(cpf):
    try:
        cpf_exists = await cpf_existe(cpf)
        if cpf_exists:
            return {"message": "Ja existe um cliente com esse CPF "}, 200
        return {"message": "Nao existe um cliente com esse CPF "}, 404
    except Exception:
        return {"message": "Conexão perdida durante consulta ao banco"}, 503


@app.route("/verifica-email/<email>")
async def veirfica_email(email):
    try:
        email_exists = await email_existe(email)
        if email_exists:
            return {"message": "Ja existe um cliente com esse E-mail"}, 200
        return {"message": "Nao existe um cliente com esse E-mail"}, 404
    except Exception:
        return {"message": "Conexão perdida durante consulta ao banco"}, 503


@app.route("/pedidos", methods=['POST'])
async def faz_pedido():
    pedido = request.json
    cliente_id = pedido['cliente_id']
    formas_pagamento = pedido['formas_pagamento']
    itens_pedido = pedido['itens_pedido']

    try:
        retorno = await inserir_pedido(cliente_id, formas_pagamento, itens_pedido)
        if retorno is not None:
            return {"message": "pedido efetuado com sucesso!", "pedido_id": retorno}, 200
        else:
            return {"message": "erro ao inserir pedido"}, 500
    except Exception:
        return {"message": "Conexão perdida durante consulta ao banco"}, 503


# lembrar de comentar essa parte quando for subir para o heroku
# if __name__ == "__main__":
#     app.run("localhost", port=5000, debug=True)
