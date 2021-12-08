import sys
from api import server, db

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    host = '0.0.0.0' if len(sys.argv) > 1 else '127.0.0.1'
    server.run(host=host, port=port)