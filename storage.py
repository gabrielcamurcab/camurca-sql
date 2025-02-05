import pickle
import os

class CamurcaSQLStorage:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.db = {}


    def create_database(self):
        if os.path.exists(self.db_filename):
            raise FileExistsError(f"O banco de dados '{self.db_filename}' já existe.")
        with open(self.db_filename, 'wb') as f:
            pickle.dump(self.db, f)
        print(f"Banco de dados '{self.db_filename}' criado com sucesso!")

    def open_database(self):
        if not os.path.exists(self.db_filename):
            raise FileNotFoundError(f"O banco de dados '{self.db_filename}' não existe.")
        with open(self.db_filename, 'rb') as f:
            self.db = pickle.load(f)
        print(f"O banco de dados '{self.db_filename}' foi carregado com sucesso!")

    def save_database(self):
        with open(self.db_filename, 'wb') as f:
            pickle.dump(self.db, f)
        print(f"Banco de dados '{self.db_filename}' salvo com sucesso!")
