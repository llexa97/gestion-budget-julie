import os
from app import create_app, db
from app.models import Period, Transaction

app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Rendre les modèles disponibles dans le shell Flask"""
    return {'db': db, 'Period': Period, 'Transaction': Transaction}


if __name__ == "__main__":
    app.run(debug=True, port=5001)
