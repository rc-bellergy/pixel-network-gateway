from pixel_network.auth import get_jwt_token
import os
from dotenv import load_dotenv

load_dotenv()

graphql_url = os.getenv('GRAPHQL_URL')
user_login = os.getenv('USER_LOGIN')
user_password = os.getenv('USER_PASSWORD')

jwt_token = get_jwt_token(user_login, user_password, graphql_url)

# print(jwt_token)
