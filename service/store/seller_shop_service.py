import traceback

class SellerShopService:
    """ Business Layer

        Attributes:
            seller_shop_dao: SellerShopDao 클래스

        Author: 고수희

        History:
            2021-01-01(고수희): 초기 생성
    """

    def __init__(self, seller_shop_dao):
        self.seller_shop_dao = seller_shop_dao

    def get_seller_info_service(self, connection, data):
        """ GET 메소드: 셀러 상세 페이지에 출력되는 셀러 정보

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 고수희

        Returns:
            return (): 셀러 정보 반환

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값

        History:
            2021-01-01(고수희): 초기 생성
        """
        try:
            #셀러정보 정보 조회
            return self.seller_shop_dao.get_seller_info_dao(connection, data)

        except KeyError:
            traceback.print_exc()
            raise KeyError('key_error')

    def get_seller_product_search_service(self, connection, data):
        """ GET 메소드: 셀러 상세 페이지에서 검색 시 출력되는 상품 정보

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 고수희

        Returns:
            return (): 검색 시 출력되는 정보 반환

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값

        History:
            2021-01-02(고수희): 초기 생성
        """
        try:
            #셀러 상품 검색
            return self.seller_shop_dao.get_seller_product_search_dao(connection, data)

        except KeyError:
            traceback.print_exc()
            raise KeyError('key_error')

    def get_seller_category_service(self, connection, data):
        """ GET 메소드: 셀러 상세 페이지에 출력되는 카테고리 정보

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 고수희

        Returns:
            return (): 조회한 상품 정보와 상품 품절 여부 반환

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값

        History:
            2021-01-02(고수희): 초기 생성
        """
        try:
            #셀러 카테고리 조회
            return self.seller_shop_dao.get_seller_category_dao(connection, data)

        except KeyError:
            traceback.print_exc()
            raise KeyError('key_error')

    def get_seller_product_list_service(self, connection, data):
        """ GET 메소드: 셀러 상세 페이지에 출력되는 상품 정보 리스트

        Args:
            connection: 데이터베이스 연결 객체
            data      : View 에서 넘겨받은 dict 객체

        Author: 고수희

        Returns:
            return (): 조회한 상품 정보 리스트 출력

        Raises:
            400, {'message': 'key error',
            'errorMessage': 'key_error'} : 잘못 입력된 키값

        History:
            2021-01-02(고수희): 초기 생성
        """
        try:
            #셀러 상품 조회
            return self.seller_shop_dao.get_seller_product_list_dao(connection, data)

        except KeyError:
            traceback.print_exc()
            raise KeyError('key_error')
