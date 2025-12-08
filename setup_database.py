"""
Script para configurar PostgreSQL automáticamente para Abogadai
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

print("=" * 60)
print("CONFIGURACIÓN AUTOMÁTICA DE POSTGRESQL PARA ABOGADAI")
print("=" * 60)
print()

# Pedir solo la contraseña del superusuario postgres
print("Para configurar PostgreSQL necesito la contraseña del superusuario.")
print()
postgres_password = input("Contraseña del usuario 'postgres': ").strip()

print()
print("Configurando PostgreSQL...")
print("-" * 60)

try:
    # Paso 1: Conectar como superusuario
    print("\n[1/5] Conectando como superusuario...")
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password=postgres_password
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    print("      ✓ Conectado como superusuario")

    # Paso 2: Verificar/Crear usuario abogadai_user
    print("\n[2/5] Configurando usuario 'abogadai_user'...")
    try:
        # Intentar eliminar el usuario si existe
        cur.execute("DROP USER IF EXISTS abogadai_user;")
        print("      - Usuario anterior eliminado (si existía)")
    except:
        pass

    # Crear el usuario
    cur.execute("""
        CREATE USER abogadai_user
        WITH PASSWORD 'abogadai123'
        CREATEDB
        LOGIN;
    """)
    print("      ✓ Usuario 'abogadai_user' creado")

    # Paso 3: Eliminar base de datos anterior si existe
    print("\n[3/5] Limpiando base de datos anterior...")
    try:
        # Cerrar todas las conexiones a la base de datos
        cur.execute("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'abogadai_db'
            AND pid <> pg_backend_pid();
        """)
        cur.execute("DROP DATABASE IF EXISTS abogadai_db;")
        print("      ✓ Base de datos anterior eliminada")
    except Exception as e:
        print(f"      - No había base de datos anterior")

    # Paso 4: Crear nueva base de datos con UTF-8
    print("\n[4/5] Creando base de datos 'abogadai_db' con UTF-8...")
    cur.execute("""
        CREATE DATABASE abogadai_db
        WITH
        OWNER = abogadai_user
        ENCODING = 'UTF8'
        LC_COLLATE = 'C'
        LC_CTYPE = 'C'
        TEMPLATE = template0;
    """)
    print("      ✓ Base de datos creada con encoding UTF-8")

    # Paso 5: Otorgar todos los privilegios
    print("\n[5/5] Otorgando permisos...")
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE abogadai_db TO abogadai_user;")
    print("      ✓ Permisos otorgados")

    cur.close()
    conn.close()

    print()
    print("=" * 60)
    print("✓ CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print()
    print("Credenciales configuradas:")
    print("  Usuario:      abogadai_user")
    print("  Contraseña:   abogadai123")
    print("  Base de datos: abogadai_db")
    print("  Encoding:     UTF-8")
    print()

    # Probar la conexión con el nuevo usuario
    print("Probando conexión con el nuevo usuario...")
    test_conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="abogadai_db",
        user="abogadai_user",
        password="abogadai123",
        client_encoding='UTF8'
    )
    test_cur = test_conn.cursor()
    test_cur.execute("SELECT version();")
    version = test_cur.fetchone()[0]
    print(f"✓ Conexión exitosa!")
    print()
    test_cur.close()
    test_conn.close()

    print("Ahora puedes ejecutar el backend:")
    print("  uvicorn app.main:app --reload --port 8000")
    print()

except psycopg2.OperationalError as e:
    print()
    print("=" * 60)
    print("✗ ERROR DE CONEXIÓN")
    print("=" * 60)
    print()
    print(str(e))
    print()
    print("Posibles causas:")
    print("  1. PostgreSQL no está corriendo")
    print("  2. La contraseña del usuario 'postgres' es incorrecta")
    print("  3. PostgreSQL está en un puerto diferente al 5432")
    print()
    print("Para verificar:")
    print("  - Abre pgAdmin4 y asegúrate de poder conectarte")
    print("  - Verifica que PostgreSQL esté corriendo (Services en Windows)")
    print()

except Exception as e:
    print()
    print("=" * 60)
    print("✗ ERROR INESPERADO")
    print("=" * 60)
    print()
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    print()
    import traceback
    traceback.print_exc()

print()
input("Presiona Enter para salir...")
