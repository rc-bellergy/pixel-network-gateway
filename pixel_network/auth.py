import requests

def get_jwt_token(user_login, user_password, graphql_url):
    try:
        # First mutation to get the refresh token
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
        """ % (
            user_login,
            user_password,
        )

        # Set the headers for the request
        headers = {"Content-Type": "application/json"}

        # Make the request and get the refresh token
        response = requests.post(
            graphql_url, json={"query": refresh_token_mutation}, headers=headers
        )
        response.raise_for_status()

        refresh_token_data = response.json()
        if "errors" in refresh_token_data:
            raise Exception(f"GraphQL error: {refresh_token_data['errors']}")

        refresh_token = refresh_token_data["data"]["authRefreshToken"]["refreshToken"][
            "token"
        ]

        # Second mutation to get the JWT token using the refresh token
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

        # Make the request and get the JWT token
        response = requests.post(
            graphql_url,
            json={
                "query": access_token_mutation,
                "variables": {"token": refresh_token},
            },
            headers=headers,
        )
        response.raise_for_status()

        access_token_data = response.json()
        if "errors" in access_token_data:
            raise Exception(f"GraphQL error: {access_token_data['errors']}")

        # Extract and return the JWT token
        jwt_token = access_token_data["data"]["authAccessToken"]["jwtToken"]
        return jwt_token

    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
    except Exception as e:
        print(f"Error: {e}")

    return None
