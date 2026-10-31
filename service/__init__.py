"""
Package: service
Package for the application models and service routes
This module initializes the Flask app and applies security headers
"""
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

# Create Flask application
app = Flask(__name__)
app.config.from_object("config")

# Set up Talisman security headers
talisman = Talisman(app, force_https=False)

# Set up CORS policies
CORS(app)

# Import routes and models after app creation
from service import routes, models  # noqa: F401, E402
from service.common import log_handlers, error_handlers  # noqa: F401, E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")
