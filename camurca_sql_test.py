from storage import CamurcaSQLStorage
from model import CamurcaSQLModel
from query import CamurcaSQLQuery

storage = CamurcaSQLStorage('meu_bd.bin')
storage.save_database()

model = CamurcaSQLModel(storage)
query_processor = CamurcaSQLQuery(model)

try:
    query_processor.execute("CREATE TABLE usuarios (id INT, nome TEXT, idade INT)")
except ValueError as e:
    print(f"Erro ao criar tabela: {e}")

try:
    query_processor.execute("INSERT INTO usuarios (id, nome, idade) VALUES (1, 'Alice', 25)")
    query_processor.execute("INSERT INTO usuarios (id, nome, idade) VALUES (2, 'Bob', 30)")
except ValueError as e:
    print(f"Erro ao inserir dados: {e}")

try:
    resultado = query_processor.execute("SELECT * FROM usuarios")
    print("Usuários após inserção:", resultado)
except ValueError as e:
    print(f"Erro ao selecionar dados: {e}")

try:
    query_processor.execute("UPDATE usuarios SET idade = 26 WHERE id = 1")
    resultado = query_processor.execute("SELECT * FROM usuarios")
    print("Usuários após atualização:", resultado)
except ValueError as e:
    print(f"Erro ao atualizar dados: {e}")

try:
    query_processor.execute("DELETE FROM usuarios WHERE id = 2")
    resultado = query_processor.execute("SELECT * FROM usuarios")
    print("Usuários após deleção:", resultado)
except ValueError as e:
    print(f"Erro ao deletar dados: {e}")