from app import create_app
from app.utils.background_worker import background_worker
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = create_app()

# Start background worker
background_worker.start()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        background_worker.stop()


