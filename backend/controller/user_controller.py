import pymysql

from flask      import request
from connection import get_connection

def create_user_endpoints(app, services):
    user_service = services.user_service

    @app.route('/sign-up', methods = ['POST'])
    def sign_up():

        """
        회원가입 API [POST]

        Args:

        user                : 셀러 id
        password            : 비밀번호
        phone_number        : 핸드폰번호
        seller_attribute_id : 셀러 정보 id (쇼핑몰 : 1, 마켓 : 2, 로드샵 : 3, 디자이너브랜드 : 4, 제너럴브랜드 : 5, 내셔널브랜드 : 6, 뷰티 : 7)
        name                : 셀러명 (상호)
        eng_name            : 영문 셀러명(영문상호)
        service_number      : 고객센터 전화번호
        site_url            : 사이트 URL

        Returns:

        success   : 200
        key error          : {message : KEY_ERROR}, code : 400
        셀러 ID 중복        : {message : USER_ALREADY_EXISTS}, code : 400
        비밀번호 형식 위반   : {message : PASSWORD_VALIDATION_ERROR}, code : 400
        핸드폰번호 형식 위반 : {message : PHONE_NUMBER_VALIDATION_ERROR}, code : 400

        """

        db_connection = None    
        try:
            db_connection = get_connection()
            new_user = request.json
            if db_connection:
                sign_up_response = user_service.create_new_user(new_user, db_connection)
                db_connection.commit()
                return sign_up_response          

        except pymysql.err.InternalError:

            if db_connection: 
                db_connection.rollback()      

            return {'message' : 'DATABASE_SERVER_ERROR'}, 500
        
        except pymysql.err.OperationalError:              
            return {'message' : 'DATABASE_ACCESS_DENIED'}, 500

        finally:
            if db_connection:
                db_connection.close() 

    @app.route('/sign-in', methods=['POST'])
    def sign_in():

        """
        로그인 API [POST]
        
        Args:

        user        : 셀러 id
        password    : 비밀번호
        
        Returns:

        Success     : {access_token : token}, 200
        Key error   : {message : KEY_ERROR}, status code : 400
        """
        
        db_connection = None 
        get_user = request.json
        try:
            db_connection = get_connection()
            if db_connection:
                sign_in_response = user_service.check_user(get_user, db_connection)
                db_connection.close()
                return sign_in_response

        except pymysql.err.InternalError:
            return jsonify({'message' : 'DATABASE_SERVER_ERROR'}), 500

        except pymysql.err.OperationalError:
            return jsonify({'message' : 'DATABASE_ACCESS_DENIED'}), 500

        finally:

            if db_connection:
                db_connection.close()
               