# Database
from src.database.db_postgres import get_connection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.ValidatorModel import ValidatorModel


class AdditionalPermissionService():

    @classmethod
    def get_permisssions(cls):
        try:
            connection = get_connection()
            validators = []
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, type, dni FROM public.validators')
                resultset = cursor.fetchall()
                for row in resultset:
                    # print('row', row)
                    validator = ValidatorModel(
                        int(row[0]),
                        row[1],
                        row[2],
                    )
                    validators.append(validator.to_json())
            connection.close()
            return validators
        except Exception as e:
            Logger.add_to_log("error", str(e))
            # Logger.add_to_log("error", traceback.format_exc())