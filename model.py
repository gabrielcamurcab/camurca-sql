class CamurcaSQLModel:
    def __init__(self, storage):
        self.storage = storage
        self.db = storage.db

    def create_table(self, table_name, columns):
        if table_name in self.db:
            raise ValueError(f"A tabela '{table_name}' já existe.")
        self.db[table_name] = {"colunas": columns, "dados": []}
        self.storage.save_database()
        print(f"Tabela '{table_name}' salva com sucesso!0")

    def insert(self, table_name, values):
        if table_name not in self.db:
            raise ValueError(f"Tabela '{table_name}' não existe neste banco de dados")
        table = self.db[table_name]
        print(table['colunas'])
        if len(values) != len(table['colunas']):
            raise ValueError("O número de valores não corresponde ao número de colunas")
        table["dados"].append(values)
        self.storage.save_database()
        print(f"Dados inseridos na tabela '{table_name}' com sucesso!")

    def select(self, table_name):
        if table_name not in self.db:
            raise ValueError(f"Tabela '{table_name}' não existe neste banco de dados")
        return self.db[table_name]["dados"]
    
    def update(self, table_name, where_condition, new_values):
        if table_name not in self.db:
            raise ValueError(f"Tabela '{table_name}' não existe neste banco de dados")
        table = self.db[table_name]
        updated_rows = 0
        for row in table["dados"]:
            print(f"Comparando {row} com condição {where_condition(row)}")  
            if where_condition(row):
                print(f"Atualizando: {row}")  # Depuração
                for column, new_value in new_values.items:
                    row[column] = new_value
                updated_rows += 1
        self.storage.save_database()
        print(f"{updated_rows} linhas atualizadas na tabela '{table_name}'")

    def delete(self, table_name, where_conditions):
        if table_name not in self.db:
            raise ValueError(f"Tabela '{table_name}' não existe neste banco de dados")
        table = self.db[table_name]
        table["dados"] = [row for row in table["dados"] if not where_conditions(row)]
        self.storage.save_database()
        print(f"Linha deletadas da tabela '{table_name}'")