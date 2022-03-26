from sqlalchemy import text, engine_from_config, create_engine
from .config import config

#engine = create_engine('mysql://root:dinossauro12@localhost/mais_fit')
engine = engine_from_config(config, prefix='db.')


def lista_sabores_ativos():
    with engine.connect() as con:
        statement = text("""SELECT nome, descricao, valor, link, ativo 
                            FROM sabores
                            WHERE ativo = 'SIM'""")
        rs = con.execute(statement)
        sabores = []
        item = rs.fetchone()
        while (item != None):
            sabores.append(dict(item))
            item = rs.fetchone()
    return sabores

# if __name__ == "__main__":
#     print(lista_sabores_ativos())
