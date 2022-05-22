from config import config

from sqlalchemy import text, engine_from_config
from datetime import datetime
import jwt


engine = engine_from_config(config, prefix='db.')


def lista_sabores_ativos():
    with engine.connect() as con:
        statement = text("""SELECT nome, descricao, link, ativo 
                            FROM marmitas
                            WHERE ativo = 1""")
        rs = con.execute(statement)
        sabores = []
        item = rs.fetchone()
        while (item != None):
            sabores.append(dict(item))
            item = rs.fetchone()
    return sabores


def lista_pagamentos_ativo():
    with engine.connect() as con:
        statement = text("""SELECT id, descricao, link 
                            FROM meios_pagamento
                            WHERE ativo = 1""")
        rs = con.execute(statement)
        pagamento = []
        item = rs.fetchone()
        while (item != None):
            pagamento.append(dict(item))
            item = rs.fetchone()
    return pagamento

def cadastrar_cliente(dados):
    nome_completo = dados["nome_completo"]
    cpf = dados["cpf"]
    nascimento = dados["nascimento"]
    genero = dados["genero"]
    celular = dados["celular"]
    cep = dados["cep"]
    logradouro = dados["logradouro"]
    numero = dados["numero"]
    complemento = dados["complemento"]
    bairro = dados["bairro"]
    email = dados["email"]
    senha = dados["senha"]
    senha = jwt.encode({"senha":"{0}".format(senha)}, "secret", algorithm="HS256")
    with engine.connect() as con:
        statement = text("""INSERT INTO clientes 
            (   nome_completo, cpf, nascimento, genero, celular, cep, logradouro, numero, 
                complemento, bairro, email, senha ) values
            (:nome_completo, :cpf, :nascimento, :genero, :celular, :cep, :logradouro, 
            :numero, :complemento, :bairro, :email, :senha)
        """)
        con.execute(statement, nome_completo=nome_completo, cpf=cpf, 
                    nascimento=nascimento, genero=genero, celular=celular, cep=cep, 
                    logradouro=logradouro, numero=numero, 
                    complemento=complemento, bairro=bairro, email=email, senha=senha)

def listar_clientes():
    """
        Lista todos os clientes da base de dados baseado em filtros
    """
    #TODO -> precisamos implementar os filtros de buscas
    with engine.connect() as con:
        statement = text("""SELECT nome_completo, cpf, nascimento, genero, celular, cep, logradouro, numero, complemento, bairro, email, senha 
                            FROM clientes"""
                            )
        rs = con.execute(statement)
        clientes = []
        item = rs.fetchone()
        while (item != None):
            clientes.append(dict(item))
            item = rs.fetchone()
    return clientes


def cpf_existe(cpf):
    """
        Verifica se já existe um cpf cadastrado no banco
    """
    with engine.connect() as con:
        statement = text("""SELECT cpf 
                            FROM clientes
                            WHERE cpf = :cpf""")
        rs = con.execute(statement, cpf=cpf)
        item = rs.fetchone()
        if item:
            return True
        else:
            return False

def email_existe(email):
    """
        Verifica se já existe um e-mail cadastrado no banco
    """
    with engine.connect() as con:
        statement = text("""SELECT email 
                            FROM clientes
                            WHERE email = :email""")
        rs = con.execute(statement, email=email)
        item = rs.fetchone()
        if item:
            return True
        else:
            return False

def inserir_pedido(cliente_id, formas_pagamento, itens_pedido):

    data_emissao = datetime.now()

    with engine.connect() as con:
        # inserindo pedido
        statement = text (
            """
            INSERT INTO pedidos (status, data_emissao, id_cliente)
            VALUES (:status, :data_emissao, :id_cliente)
            """
        )
        con.execute(statement, status="iniciado", data_emissao=data_emissao,
        id_cliente=cliente_id)
        # TODO -> verificar uma forma melhor de buscar o id do pedido
        # pode acontecer de pedidos serem feitos ao mesmo tempo, o que pode
        # causar um retorno errado da função abaixo.
        id_pedido = retorna_id_ultimo_pedido()
        # após inserir o pedido, vou inserir as formas de pagamento do pedido
        inserir_formas_pagamento(formas_pagamento, id_pedido)
        # após, devemos inserir os itens do pedido
        inserir_itens_pedido(itens_pedido, id_pedido)
    return id_pedido

def retorna_id_ultimo_pedido():
    with engine.connect() as con:
        statement = text (
            """
                SELECT MAX(id) as maxId FROM pedidos
            """
        )
        rs = con.execute(statement)
        id_pedido = rs.fetchone()
    return id_pedido[0]


def inserir_formas_pagamento(formas_pagamento, id_pedido):
    with engine.connect() as con:
        for meios_pagamento in formas_pagamento:
            statement = text (
                """
                    INSERT INTO formas_pagamento (qtd, id_meios_pagamento, id_pedido)
                    VALUES (:qtd, :id_meios_pagamento, :id_pedido)
                """
            )
            con.execute(statement, qtd=meios_pagamento['qtd_pagamento'], 
                        id_meios_pagamento=meios_pagamento['meio_pagamento_id'], 
                        id_pedido=id_pedido)


def inserir_itens_pedido(itens_pedido, id_pedido):
    with engine.connect() as con:
        for kit in itens_pedido:
            statement = text (
                """
                    INSERT INTO itens_pedidos (qtd, preco, id_pedido, id_kit)
                    VALUES (:qtd, :preco, :id_pedido, :id_kit)
                """
            )
            con.execute(statement, qtd=kit['qtd_kit'], preco=kit['preco'],
                        id_pedido=id_pedido, id_kit=kit['kit_id'])
            for marmita in kit["marmitas"]:
                statement = text (
                    """
                        INSERT INTO itens_kits (qtd_marmita, id_marmita, id_kit, id_pedido)
                        VALUES (:qtd_marmita, :id_marmita, :id_kit, :id_pedido)

                    """
                )
                con.execute(statement, qtd_marmita=marmita["qtd_marmita"],
                            id_marmita=marmita['marmita_id'], 
                            id_kit=kit['kit_id'],
                            id_pedido=id_pedido)
