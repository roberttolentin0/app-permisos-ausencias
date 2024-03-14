import traceback

# Database
from src.database.db_postgres import PGConnection
from src.database.db_postgres import RhDBConnection
from src.utils.Logger import Logger
# from src.utils.DateFormat import DateFormat
# Models
# from src.models.PermissionModel import Permission

connectionDB = PGConnection()
connectionRhDB = RhDBConnection()


class EmployeeService():

    @classmethod
    def get_name_employee(cls, dni):
        '''Obtiene datos de la DB de RRHH'''
        try:
            connection = connectionRhDB.connect()
            employee = {}
            with connection.cursor() as cursor:
                query = f"""
                            SELECT dni, fullname, lastname, surname
                            FROM employee
                            WHERE dni = '{dni}'
                        """
                cursor.execute(query)
                resultset = cursor.fetchall()
                print('resultset', resultset)
                for row in resultset:
                    print('row', row)
                    employee['dni'] = row[0]
                    employee['full_name'] = f'{row[1]} {row[2]} {row[3]}'
            connectionRhDB.close()
            return employee
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def create_employee(cls, employee):
        '''Crea en nuestra DB Local'''
        print('create_employee', employee.to_json())
        try:
            connection = connectionDB.connect()
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO public.employees(dni, full_name)
	                            VALUES (%s, %s);""",
                                (employee.dni, employee.full_name))
                affected_rows = cursor.rowcount
                connection.commit()
            connectionDB.close()
            return affected_rows
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())