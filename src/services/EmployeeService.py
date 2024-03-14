import traceback

# Database
from src.database.db_postgres import RhDBConnection
from src.utils.Logger import Logger
# from src.utils.DateFormat import DateFormat
# Models
# from src.models.PermissionModel import Permission

connectionRhDB = RhDBConnection()


class EmployeeService():

    @classmethod
    def get_name_employee(cls, dni):
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
