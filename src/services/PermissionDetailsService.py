import traceback
from datetime import datetime
# Database
from src.database.db_postgres import PGConnection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.PermissionDetailsModel import PermissionDetailsModel
# from src.models.AdditionalPermissionModel import ViewAdditionalPermissionModel

connectionDB = PGConnection()

class PermissionDetailsService():

    # @classmethod
    # def get_additional_permisssions_by_id(cls, permission_id):
    #     try:
    #         connection = connectionDB.connect()
    #         additional_permissions = []
    #         with connection.cursor() as cursor:
    #             cursor.execute(
    #                 """SELECT
    #                 permission_id,
    #                 permission_date,
    #                 start_time,
    #                 return_time,
    #                 reason,
    #                 status,
    #                 end_time,
    #                 additional_reason,
    #                 additional_time
	#                 FROM public.view_additional_permissions WHERE permission_id = %s"""
    #                 ,(permission_id))
    #             resultset = cursor.fetchall()
    #             for row in resultset:
    #                 print('row', row)
    #                 additional_permission = ViewAdditionalPermissionModel(
    #                     int(row[0]),
    #                     row[1],
    #                     row[2],
    #                     row[3],
    #                     row[4],
    #                     row[5],
    #                     row[6],
    #                     row[7],
    #                     row[8]
    #                 )
    #                 additional_permissions.append(additional_permission.to_json())
    #         connection.close()
    #         return additional_permissions
    #     except Exception as e:
    #         Logger.add_to_log("error", str(e))
    #         Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def create_permission_detail(cls, permission_detail):
        print('create_permission_detail', permission_detail.to_json())
        try:
            connection = connectionDB.connect()
            with connection.cursor() as cursor:
                new_return_time= datetime.strptime(permission_detail.return_time, "%H:%M").time()
                cursor.execute("""INSERT INTO public.permission_details
                                (permission_id, reason, return_time, created_at)
                                VALUES (%s, %s, %s, %s)""",
                                (permission_detail.permission_id,
                                 permission_detail.reason,
                                 new_return_time,
                                 datetime.now()))
                affected_rows = cursor.rowcount
                connection.commit()
            connectionDB.close()
            return affected_rows
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())