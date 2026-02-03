import os
import logging
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend')
    app = Flask(__name__, static_folder=frontend_path, static_url_path='')

    # JWT Configuration - ensure 32+ byte key
    jwt_secret = os.environ.get("JWT_SECRET_KEY")
    if not jwt_secret or len(jwt_secret) < 32:
        logger.warning("JWT_SECRET_KEY too short or missing, using secure default for development")
        jwt_secret = "dev-secret-key-change-in-production-minimum-32-chars-long!!"
    
    app.config["JWT_SECRET_KEY"] = jwt_secret

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

    @app.route('/<path:filename>')
    def serve_static(filename):
        return send_from_directory(frontend_path, filename)
    
    # TEMPORARY: Reset DB endpoint (remove after testing)
    @app.route('/reset-db', methods=['DELETE'])
    def reset_db():
        try:
            db_path = os.getenv("SQLITE_DB_PATH", "tickets.db")
            if os.path.exists(db_path):
                os.remove(db_path)
                logger.info(f"Deleted {db_path}")
            return {"msg": "DB reset. Restart app to reinitialize."}, 200
        except Exception as e:
            return {"error": str(e)}, 500
    
    logger.info("Flask app initialized successfully with JWT_SECRET_KEY length: %d", len(jwt_secret))
    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)