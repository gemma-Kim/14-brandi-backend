from flask import jsonify, g
from flask.views import MethodView
from flask_request_validator import (
    PATH,
    Param,
    JSON,
    validate_params
)

from utils.connection import get_connection
from utils.custom_exceptions import DatabaseCloseFail
from utils.rules import DecimalRule, EmailRule, PostalCodeRule, PhoneRule
from utils.decorator import signin_decorator


class StoreOrderView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service: CartItemService 클래스

    Author: 고수희

    History:
        2020-12-30(고수희): 초기 생성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @signin_decorator(True)
    @validate_params(
        Param('order_id', PATH, int)
    )
    def get(self, *args):
        """ GET 메소드: 해당 유저가 직전에 마친 결제 정보를 조회
        결제가 완료된 페이지에서 확인하는 정보다.

        order_id에 해당되는 결제 상품 정보를 테이블에서 조회 후 가져옴

        Args: args = ('account_id', 'cart_id')

        Author: 고수희

        Returns:
            #통화에 대한 정의와 정수로 변환
            {
                "message": "success",
                "result": {
                    "order_number": "20210101000001000",
                    "total_price": 8000.0
                }
            }

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값
            400, {'message': 'cart item does not exist error',
            'errorMessage': 'cart_item_does_not_exist'} : 장바구니 상품 정보 조회 실패
            400, {'message': 'unable to close database',
            'errorMessage': 'unable_to_close_database'}: 커넥션 종료 실패
            500, {'message': 'internal server error',
            'errorMessage': format(e)}) : 서버 에러

        History:
            2020-12-28(고수희): 초기 생성
            2020-12-30(고수희): 1차 수정 - 데코레이터 추가, 사용자 권한 체크
            2021-01-02(고수희): decorator 수정
        """
        data = {
            "order_id": args[0],
            "user_id": g.account_id,
            "user_permission": g.permission_type_id
        }
        
        try:
            connection = get_connection(self.database)
            store_order_info = self.service.get_store_order_service(connection, data)
            return jsonify({'message': 'success', 'result': store_order_info})

        except Exception as e:
            raise e
        finally:
            try:
                if connection:
                    connection.close()
            except Exception:
                raise DatabaseCloseFail('database close fail')


class StoreOrderAddView(MethodView):
    """ Presentation Layer

    Attributes:
        database: app.config['DB']에 담겨있는 정보(데이터베이스 관련 정보)
        service : StoreOrderService 클래스

    Author: 고수희

    History:
        2020-12-30(고수희): 초기 생성
    """

    def __init__(self, service, database):
        self.service = service
        self.database = database

    @signin_decorator(True)
    @validate_params(
        Param('cartId', JSON, int),
        Param('productId', JSON, int),
        Param('stockId', JSON, int),
        Param('quantity', JSON, int),
        Param('originalPrice', JSON,int),
        Param('sale', JSON, str, rules=[DecimalRule()]),
        Param('discountedPrice', JSON, int),
        Param('totalPrice', JSON, int),
        Param('soldOut', JSON, bool),
        Param('senderName', JSON, str),
        Param('senderPhone', JSON, str, rules=[PhoneRule()]),
        Param('senderEmail', JSON, str, rules=[EmailRule()]),
        Param('recipientName', JSON, str),
        Param('recipientPhone', JSON, str, rules=[PhoneRule()]),
        Param('address1', JSON, str),
        Param('address2', JSON, str),
        Param('postNumber', JSON, str, rules=[PostalCodeRule()]),
        Param('deliveryId', JSON, int),
        Param('deliveryMemo', JSON, str, required=False),
    )
    def post(self, *args):
        """POST 메소드: 장바구니 상품 생성

        Args: args = (
        'user_id',
        'user_permission',
        'cart_id',
        'product_id',
        'stock_id',
        'quantity',
        'original_price',
        'sale',
        'discounted_price',
        'total_price',
        'sold_out',
        'sender_name',
        'sender_phone',
        'sender_email',
        'recipient_name',
        'recipient_phone',
        'address1',
        'address2',
        'post_number',
        'delivery_memo_type_id',
        'delivery_content'
        )

        Author: 고수희

        Returns:
            200, {'message': 'success'} : 결제 성공

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값



            400, {'message': 'unable to close database',
            'errorMessage': 'unable_to_close_database'} : 커넥션 종료 실패
            403, {'message': 'customer permission denied',
            'errorMessage': 'customer_permission_denied'} : 사용자 권한이 아님
            500, {'message': 'internal server error',
            'errorMessage': format(e)}) : 서버 에러

        History:
            2020-12-30(고수희): 초기 생성
        """
        data = {
            'user_id': g.account_id,
            'user_permission': g.permission_type_id,
            'cart_id': args[0],
            'product_id': args[1],
            'stock_id': args[2],
            'quantity': args[3],
            'original_price': args[4],
            'sale': args[5],
            'discounted_price': args[6],
            'total_price': args[7],
            'sold_out': args[8],
            'sender_name': args[9],
            'sender_phone': args[10],
            'sender_email': args[11],
            'recipient_name': args[12],
            'recipient_phone': args[13],
            'address1': args[14],
            'address2': args[15],
            'post_number': args[16],
            'delivery_memo_type_id': args[17],
            'delivery_content': args[18],
        }

        try:
            connection = get_connection(self.database)
            order_id = self.service.post_order_service(connection, data)
            connection.commit()
            return {'message': 'success', 'result': {"order_id": order_id}}, 201

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            try:
                if connection:
                    connection.close()

            except Exception:
                raise DatabaseCloseFail('database close fail')
