import re

class CamurcaSQLQuery:
    def __init__(self, model):
        self.model = model

    def execute(self, query):
        query = query.strip().lower()


        # Falta create
        if query.startswith("create table"):
            return self._create_table(query)
        elif query.startswith("select"):
            return self._select(query)
        elif query.startswith("insert"):
            return self._insert(query)
        elif query.startswith("update"):
            return self._update(query)
        elif query.startswith("delete"):
            return self._delete(query)
        else:
            raise ValueError("Comando não reconhecido.")
        
    def _create_table(self, query):
         table_name, columns = self._extract_table_create(query)
         return self.model.create_table(table_name, columns)

    def _select(self, query):
        table_name = self._extract_table_name(query)
        return self.model.select(table_name)
    
    def _insert(self, query):
        table_name, values = self._extract_insert_values(query)
        self.model.insert(table_name, values)

    def _update(self, query):
        table_name, where_condition, new_values = self._extract_update_values(query)
        self.model.update(table_name, where_condition, new_values)

    def _delete(self, query):
        table_name, where_condition = self._extract_delete_values(query)
        self.model.delete(table_name, where_condition)

    def _extract_table_create(self, query):
        match = re.search(r'create table (\w+) \((.*?)\)', query, re.IGNORECASE)
        if match:
            table_name = match.group(1)
            columns = self._parse_columns(match.group(2))
            return table_name, columns
        raise ValueError("Query CREATE TABLE mal formada.")

    def _extract_table_name(self, query):
        match = re.search(r'from (\w+)', query)
        if match:
            return match.group(1)
        raise ValueError("Tabela não encontrada na query")
    
    def _parse_columns(self, columns_str):
        columns = columns_str.split(',')
        parsed_columns = []
        for column in columns:
            column = column.strip()
            column_parts = column.split()
            col_name = column_parts[0]
            col_type = column_parts[1] if len(column_parts) > 1 else "TEXT"
            parsed_columns.append((col_name, col_type))
        return parsed_columns
    
    def _extract_insert_values(self, query):
        match = re.search(r'into (\w+) \((.*?)\) values \((.*?)\)', query)
        if match:
            table_name = match.group(1)
            values = tuple(map(str.strip, match.group(3).split(',')))
            return table_name, values
        raise ValueError("Query INSERT mal formada.")
    
    def _extract_update_values(self, query):
        print(query)
        match = re.search(r'update (\w+) set (.*?) where (.*)', query)
        if match:
            table_name = match.group(1)
            set_values = match.group(2).split(',')
            condition_str = re.sub(r"([^<>!])= ([0-9]+)", r"\1== int(\2)", match.group(3))
            where_condition = eval(f"lambda row: {condition_str}")
            new_values = tuple(map(str, [x.split('=')[1].strip for x in set_values]))
            return table_name, where_condition, new_values
        raise ValueError("Query UPDATE mal formada.")
    
    def _extract_delete_values(self, query):
        match = re.search(r'delete from (\w+) where (.*)', query)
        if match:
            table_name = match.group(1)
            condition_str = re.sub(r"([^<>!])=", r"\1==", match.group(3))
            where_condition = eval(f"lambda row: {condition_str}")
            return table_name, where_condition
        raise ValueError("Query DELETE mal formada.")