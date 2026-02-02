import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Get the absolute path to frontend directory
def create_app():             

    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend')

    app = Flask(__name__, static_folder=frontend_path, static_url_path='')

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key-dev-only")

    CORS(app)
    jwt = JWTManager(app)

    from .auth_routes import auth_bp
    from .ticket_routes import ticket_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(ticket_bp)

    # Serve frontend
    @app.route('/')          
    def serve_index():
        return send_from_directory(frontend_path, 'index.html')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)