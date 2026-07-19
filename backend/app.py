from flask_jwt_extended import set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port="0.0.0.0")
