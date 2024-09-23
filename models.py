from datetime import datetime, UTC
import database
import psycopg2
from psycopg2.extras import RealDictCursor


class ModelBase:
    def __init__(self, id=None, created_at=datetime.now(UTC), modified_at=datetime.now(UTC), active=True):
        self.id = id
        self.created_at = created_at
        self.modified_at = modified_at
        self.active = active


class Department(ModelBase):

    def __init__(self, id=None, name=None,created_at=datetime.now(UTC), modified_at=datetime.now(UTC), active=True):
        super().__init__(id=id, created_at=created_at, modified_at=modified_at, active=active)
        self.name = name

    @staticmethod
    def get_all():
        departments = []
        cursor = None
        try:
            with database.open_connection() as connection:  # abre a conexão com o banco de dados
                with connection.cursor(
                        cursor_factory=RealDictCursor) as cursor:  # abre o cursor que é um objeto da biblioteca
                    # para trabalhar com os registros do
                    # banco de dados. Vale ressaltar que o
                    # cursor_factory=RealDictCursor é para
                    # que os resultados venham como dicionário
                    cursor.execute(f'select * from department')  # executa o comando de consulta no banco de dados
                    rows = cursor.fetchall()  # fetchall permite que tragamos todos os registros da tabela

                    for row in rows:
                        d = Department(**row)  # aqui usamos o ** para pegar o dicionário e passar os parâmetros para
                        # o construtor da classe de departamento, para transformar o dicionário em
                        # nosso objeto
                        departments.append(d)  # adiciona na lista de retorno

        except psycopg2.DatabaseError as e:
            print(f'Erro ao realizar consulta {e}')

        return departments

    def save(self):
        try:
            with database.open_connection() as connection:
                with connection.cursor() as cursor:
                    command = f"insert into department (name) values ('{self.name}')"
                    cursor.execute(command)
        except psycopg2.DatabaseError as e:
            print(f'Erro ao inserir os dados {e}')


class Employee(ModelBase):

    def __init__(self, id=None, name=None, id_department=None, id_marital_status=None, id_district=None, salary=None, admission_date=None, birth_date=None, gender=None):
        super().__init__(id=id)
        self.name = name
        self.id_department = id_department 
        self.id_marital_status = id_marital_status 
        self.id_district = id_district
        self.salary = salary
        self.admission_date = admission_date
        self.birth_date = birth_date
        self.gender = gender

    @staticmethod
    def get_all():
        employees = []
        cursor = None
        try:
            with database.open_connection() as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute('SELECT id, name, id_department, id_district, id_marital_status, salary, admission_date, birth_date, gender FROM employee')
                    rows = cursor.fetchall()

                    for row in rows:
                        e = Employee(**row)
                        employees.append(e)  # adiciona na lista de retorno

        except psycopg2.DatabaseError as e:
            print(f'Erro ao realizar consulta: {e}')

        return employees

    def save(self):
        try:
            with database.open_connection() as connection:
                with connection.cursor() as cursor:
                    command = """
                        INSERT INTO employee 
                        (name, id_department, id_district, id_marital_status, salary, admission_date, birth_date, gender) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(command, (self.name, self.id_department, self.id_district, self.id_marital_status, self.salary, self.admission_date, self.birth_date, self.gender))
                    connection.commit()
        except psycopg2.DatabaseError as e:
            print(f'Erro ao inserir os dados: {e}')


class Department(ModelBase):
    def __init__(self, id=None, name=None):
        super().__init__(id=id)
        self.name = name

    @staticmethod
    def get_all():
        departments = []
        cursor = None
        try:
            with database.open_connection() as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute('SELECT id, name FROM department')
                    rows = cursor.fetchall()

                    for row in rows:
                        d = Department(**row)
                        departments.append(d)

        except psycopg2.DatabaseError as e:
            print(f'Erro ao realizar consulta: {e}')

        return departments


class MaritalStatus(ModelBase):
    def __init__(self, id=None, name=None):
        super().__init__(id=id)
        self.name = name

    @staticmethod
    def get_all():
        statuses = []
        cursor = None
        try:
            with database.open_connection() as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute('SELECT id, name FROM marital_status')
                    rows = cursor.fetchall()

                    for row in rows:
                        s = MaritalStatus(**row)
                        statuses.append(s)

        except psycopg2.DatabaseError as e:
            print(f'Erro ao realizar consulta: {e}')

        return statuses


class District(ModelBase):
    def __init__(self, id=None, name=None):
        super().__init__(id=id)
        self.name = name

    @staticmethod
    def get_all():
        districts = []
        cursor = None
        try:
            with database.open_connection() as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute('SELECT id, name FROM district')
                    rows = cursor.fetchall()

                    for row in rows:
                        d = District(**row)
                        districts.append(d)

        except psycopg2.DatabaseError as e:
            print(f'Erro ao realizar consulta: {e}')

        return districts