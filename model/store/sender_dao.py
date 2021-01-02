import traceback
import pymysql
from utils.custom_exceptions import AccountNotExist, ServerError


class SenderDao:
    """ Persistence Layer

        Attributes: None

        Author: 고수희

        History:
            2020-12-30(고수희): 초기 생성
    """

    def get_sender_info_dao(self, connection, data):
        """ 주문자 정보 조회

        Args:
            connection: 데이터베이스 연결 객체
            data   : 서비스 레이어에서 넘겨 받아 조회할 data

        Author: 고수희

        Returns:
            return {"name": "고수희",
                    "phone": "01012341234",
                    "email": "gosuhee@gmail.com",
                    }

        History:
            2020-12-30(고수희): 초기 생성
            2020-01-02(고수희): traceback 추가
        """
        sql = """
        SELECT
        name 
        , phone 
        , email 
        FROM customer_information
        WHERE account_id = %s
        ;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data['user_id'])
                result = cursor.fetchone()
                if not result:
                    result = {
                                "name":"",
                                "phone":"",
                                "email":""
                    }
                    return result
                return result

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')

    def get_user_permission_check_dao(self, connection, data):
        """사용자의 권한 조회

        Args:
            connection: 데이터베이스 연결 객체
            data      : 서비스 레이어에서 넘겨 받아 조회할 data

        Author:  고수희
        Returns: 조회된 권한 타입의 id 반환

        Raises:
            400, {'message': 'account_does_not_exist',
            'errorMessage': 'account_does_not_exist'} : 사용자 조회 실패

        History:
            2020-12-30(고수희): 초기 생성
        """

        sql = """
        SELECT permission_type_id
        FROM accounts  
        WHERE id = %s
        ;
        """
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data['user_id'])
                result = cursor.fetchone()
                if not result:
                    raise AccountNotExist('account_does_not_exist')
                return result

        except Exception:
            traceback.print_exc()
            raise ServerError('server_error')
