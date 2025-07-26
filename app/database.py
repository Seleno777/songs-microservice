import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Obtener la cadena de conexión del entorno
raw_connection_string = os.environ.get("DATABASE_URL")
if not raw_connection_string:
    raise RuntimeError("La variable de entorno DATABASE_URL no está definida. Configúrala en Azure con la cadena de conexión de tu base de datos.")

# Convertir cadena de Azure a formato SQLAlchemy compatible
params = {}
for segment in raw_connection_string.split(';'):
    if '=' in segment:
        key, value = segment.split('=', 1)
        params[key.strip().lower()] = value.strip()

server = params.get('server').replace('tcp:', '').split(',')[0]
port = params.get('server').split(',')[1] if ',' in params.get('server') else '1433'
database = params.get('initial catalog')
username = params.get('user id')
password = params.get('password')

# Crear la cadena SQLAlchemy
connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)


# Crear motor y sesión
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
