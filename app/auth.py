from datetime import timedelta
from authx import AuthX, AuthXConfig

config = AuthXConfig()
config.JWT_SECRET_KEY = "super_puper_secret_key"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

security = AuthX(config=config)