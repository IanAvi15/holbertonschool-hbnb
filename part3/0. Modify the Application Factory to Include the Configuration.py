from flask import Flask


def create_app(config_class="config.DevelopmentConfig"):
    """Create and configure a Flask application instance.

    Args:
        config_class (str): Dotted path to the configuration class.
                            Defaults to DevelopmentConfig.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    return app
