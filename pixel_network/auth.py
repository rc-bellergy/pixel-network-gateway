import os
import requests
import json

REFRESH_TOKEN_FILE = 'refresh_token.json'

def save_refresh_token(refresh_token):
    with open(REFRESH_TOKEN_FILE, 'w') as f:
        json.dump({'refresh_token': refresh_token}, f)

def load_refresh_token():
    if os.path.exists(REFRESH_TOKEN_FILE):
        with open(REFRESH_TOKEN_FILE, 'r') as f:
            data = json.load(f)
            return data.get('refresh_token')
    return None

def get_jwt_token_with_refresh_token(refresh_token, graphql_url):
    access_token_mutation = """
    mutation ($token: String!) {
        authAccessToken(input: {
          userRefreshToken: $token,
          accessTokenExpiration: 14400
        }) {
          clientMutationId
          jwtToken
        }
    }
    """
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        graphql_url,
        json={"query": access_token_mutation, "variables": {"token": refresh_token}},
        headers=headers,
    )
    response.raise_for_status()
    access_token_data = response.json()
    if "errors" in access_token_data:
        raise Exception(f"GraphQL error: {access_token_data['errors']}")
    jwt_token = access_token_data["data"]["authAccessToken"]["jwtToken"]

    print(f"JWT token: {jwt_token}") 
    return jwt_token

def get_jwt_token(user_login=None, user_password=None, graphql_url=None):
    try:
        refresh_token = load_refresh_token()

        if refresh_token:
            # Use the refresh token to get a new JWT token
            return get_jwt_token_with_refresh_token(refresh_token, graphql_url)

        if not user_login or not user_password:
            raise ValueError("User login and password must be provided if no refresh token is available")

        # Get the refresh token bu username and password
        refresh_token_mutation = """
        mutation {
            authRefreshToken(input: {
              userLogin: "%s"
              userPassword: "%s"
            }) {
              clientMutationId
              refreshToken {
                token
                id
                userId
              }
            }
        }
        """ % (user_login, user_password)

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            graphql_url, json={"query": refresh_token_mutation}, headers=headers
        )
        response.raise_for_status()
        refresh_token_data = response.json()
        if "errors" in refresh_token_data:
            raise Exception(f"GraphQL error: {refresh_token_data['errors']}")

        refresh_token = refresh_token_data["data"]["authRefreshToken"]["refreshToken"]["token"]
        save_refresh_token(refresh_token)

        # Use the refresh token to get a new JWT token
        return get_jwt_token_with_refresh_token(refresh_token, graphql_url)

    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
    except Exception as e:
        print(f"Error: {e}")

    return None
