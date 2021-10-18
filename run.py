import sys
from api import server, db

if __name__ == "__main__":
    db.create_all()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    server.run(host='0.0.0.0', port=port)