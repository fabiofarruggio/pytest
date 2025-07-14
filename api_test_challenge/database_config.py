import os
import logging
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from contextlib import contextmanager

try:
    import pyodbc
    import pymssql
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.exc import SQLAlchemyError
    HAS_DB_DEPENDENCIES = True
except ImportError:
    HAS_DB_DEPENDENCIES = False

logger = logging.getLogger(__name__)

@dataclass
class DatabaseCredentials:
    """
    Credenciales de base de datos
    """
    server: str
    database: str
    username: str
    password: str
    port: Optional[int] = None
    driver: str = "ODBC Driver 17 for SQL Server"

class DatabaseConfig:
    """
    Configuración y manejo de conexiones a base de datos para testing
    
    Soporta SQL Server, PostgreSQL y MySQL
    Configuración via variables de entorno o parámetros directos
    """
    
    def __init__(self):
        self.credentials = self._load_credentials()
        self.engine = None
        self.session_factory = None
        self._connection_tested = False
        self._is_available = False
        
    def _load_credentials(self) -> Optional[DatabaseCredentials]:
        """
        Carga las credenciales desde variables de entorno
        
        Variables de entorno soportadas:
        - DB_SERVER: Servidor de base de datos
        - DB_NAME: Nombre de la base de datos
        - DB_USER: Usuario
        - DB_PASSWORD: Contraseña
        - DB_PORT: Puerto (opcional)
        - DB_DRIVER: Driver ODBC (opcional)
        """
        server = os.getenv('DB_SERVER')
        database = os.getenv('DB_NAME')
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        port = os.getenv('DB_PORT')
        driver = os.getenv('DB_DRIVER', "ODBC Driver 17 for SQL Server")
        
        if not all([server, database, username, password]):
            logger.info("💡 Variables de DB no configuradas. Tests de DB se ejecutarán como mocked.")
            return None
            
        return DatabaseCredentials(
            server=server,
            database=database,
            username=username,
            password=password,
            port=int(port) if port else None,
            driver=driver
        )
    
    @property
    def is_configured(self) -> bool:
        """Retorna True si la configuración de DB está disponible"""
        return self.credentials is not None and HAS_DB_DEPENDENCIES
    
    @property
    def is_available(self) -> bool:
        """Retorna True si la DB está disponible y conectada"""
        if not self._connection_tested:
            self._test_connection()
        return self._is_available
    
    def _test_connection(self) -> bool:
        """
        Prueba la conexión a la base de datos
        
        Returns:
            bool: True si la conexión es exitosa
        """
        if not self.is_configured:
            self._connection_tested = True
            self._is_available = False
            return False
            
        try:
            with self.get_connection() as conn:
                result = conn.execute(text("SELECT 1")).fetchone()
                self._is_available = result is not None
                logger.info("✅ Conexión a base de datos exitosa")
                
        except Exception as e:
            logger.warning(f"⚠️  Conexión a DB falló: {str(e)}")
            self._is_available = False
            
        self._connection_tested = True
        return self._is_available
    
    def get_connection_string(self) -> str:
        """
        Genera la cadena de conexión SQL Server
        
        Returns:
            str: Cadena de conexión
        """
        if not self.credentials:
            raise ValueError("Credenciales de DB no configuradas")
            
        port_part = f",{self.credentials.port}" if self.credentials.port else ""
        
        return (
            f"mssql+pyodbc://{self.credentials.username}:{self.credentials.password}"
            f"@{self.credentials.server}{port_part}/{self.credentials.database}"
            f"?driver={self.credentials.driver.replace(' ', '+')}"
        )
    
    def get_engine(self):
        """
        Obtiene el engine de SQLAlchemy
        
        Returns:
            sqlalchemy.Engine: Engine configurado
        """
        if self.engine is None:
            if not self.is_configured:
                raise ValueError("Base de datos no configurada")
                
            try:
                connection_string = self.get_connection_string()
                self.engine = create_engine(
                    connection_string,
                    echo=False,
                    pool_pre_ping=True,
                    pool_recycle=3600
                )
                
                # Crear session factory
                self.session_factory = sessionmaker(bind=self.engine)
                
            except Exception as e:
                logger.error(f"❌ Error creando engine de DB: {str(e)}")
                raise
                
        return self.engine
    
    @contextmanager
    def get_connection(self):
        """
        Context manager para obtener conexión de base de datos
        
        Yields:
            sqlalchemy.Connection: Conexión activa
        """
        if not self.is_configured:
            raise ValueError("Base de datos no configurada")
            
        engine = self.get_engine()
        connection = engine.connect()
        
        try:
            yield connection
        finally:
            connection.close()
    
    @contextmanager
    def get_session(self):
        """
        Context manager para obtener sesión de SQLAlchemy
        
        Yields:
            sqlalchemy.orm.Session: Sesión activa
        """
        if not self.is_configured:
            raise ValueError("Base de datos no configurada")
            
        if not self.session_factory:
            self.get_engine()  # Inicializa session_factory
            
        session = self.session_factory()
        
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Tuple]:
        """
        Ejecuta una consulta SQL y retorna los resultados
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (Dict, optional): Parámetros para la consulta
            
        Returns:
            List[Tuple]: Resultados de la consulta
        """
        if not self.is_available:
            raise ValueError("Base de datos no disponible")
            
        try:
            with self.get_connection() as conn:
                result = conn.execute(text(query), params or {})
                return result.fetchall()
                
        except SQLAlchemyError as e:
            logger.error(f"❌ Error ejecutando query: {str(e)}")
            raise
    
    def validate_person_exists(self, person_id: int) -> bool:
        """
        Valida que una persona existe en la tabla Test.Worldsys
        
        Args:
            person_id (int): ID de la persona a validar
            
        Returns:
            bool: True si la persona existe
        """
        if not self.is_available:
            return False
            
        try:
            query = "SELECT COUNT(*) FROM Test.Worldsys WHERE personId = :person_id"
            results = self.execute_query(query, {"person_id": person_id})
            count = results[0][0] if results else 0
            
            exists = count > 0
            logger.info(f"🔍 Person ID {person_id} {'encontrado' if exists else 'no encontrado'} en DB")
            return exists
            
        except Exception as e:
            logger.error(f"❌ Error validando person_id {person_id}: {str(e)}")
            return False
    
    def get_person_data(self, person_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene los datos de una persona desde la base de datos
        
        Args:
            person_id (int): ID de la persona
            
        Returns:
            Dict[str, Any]: Datos de la persona o None si no existe
        """
        if not self.is_available:
            return None
            
        try:
            query = "SELECT DISTINCT * FROM Test.Worldsys WHERE personId = :person_id"
            results = self.execute_query(query, {"person_id": person_id})
            
            if not results:
                return None
                
            # Assumiendo estructura básica de la tabla
            # Ajustar según la estructura real de tu tabla
            row = results[0]
            return {
                "personId": row[0],
                "firstName": row[1] if len(row) > 1 else None,
                "lastName": row[2] if len(row) > 2 else None,
                "email": row[3] if len(row) > 3 else None,
                "created_at": row[4] if len(row) > 4 else None
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo datos de person_id {person_id}: {str(e)}")
            return None

# Instancia global de configuración
db_config = DatabaseConfig() 