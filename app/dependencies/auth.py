from fastapi.security import OAuth2AuthorizationCodeBearer

oauth_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize",
    tokenUrl="https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
    scopes={"openid": "Open ID", "profile": "Profile Info"},
)

def setup_oauth(app):
    app.oauth_scheme = oauth_scheme
