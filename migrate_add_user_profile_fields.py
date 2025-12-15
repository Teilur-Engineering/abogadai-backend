"""
Migración: Agregar campos de perfil al modelo User
Fecha: 2025-12-15

Este script agrega los siguientes campos a la tabla 'users':
- identificacion (VARCHAR(50)): Cédula o NIT del usuario
- direccion (TEXT): Dirección completa del usuario
- telefono (VARCHAR(50)): Número de teléfono del usuario
- perfil_completo (BOOLEAN): Flag que indica si el perfil está completo

Estos campos permiten centralizar los datos del solicitante en el perfil del usuario
para evitar pedirlos en cada caso nuevo.
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuración de la base de datos
# NOTA: Ajusta estos valores según tu configuración
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "abogadai_db",
    "user": "abogadai_user",
    "password": "abogadai123"
}

def migrate():
    """Ejecuta la migración para agregar campos de perfil al modelo User"""
    try:
        print("="*60)
        print("MIGRACIÓN: Agregar campos de perfil al modelo User")
        print("="*60)

        # Conectar a la base de datos
        print("\n[1/5] Conectando a la base de datos...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        print("  [OK] Conexion exitosa")

        # Agregar columnas
        print("\n[2/5] Agregando columnas al modelo User...")

        columnas = [
            ("identificacion", "VARCHAR(50)"),
            ("direccion", "TEXT"),
            ("telefono", "VARCHAR(50)"),
            ("perfil_completo", "BOOLEAN DEFAULT FALSE NOT NULL")
        ]

        for columna, tipo in columnas:
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {columna} {tipo}")
                print(f"  [OK] Columna '{columna}' agregada/verificada")
            except Exception as e:
                print(f"  [WARN] Error en columna '{columna}': {e}")

        # Crear índice
        print("\n[3/5] Creando índice en identificacion...")
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_users_identificacion ON users(identificacion)")
            print("  [OK] Indice creado/verificado")
        except Exception as e:
            print(f"  [WARN] Error creando indice: {e}")

        # Verificar columnas creadas
        print("\n[4/5] Verificando columnas creadas...")
        cur.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'users'
            AND column_name IN ('identificacion', 'direccion', 'telefono', 'perfil_completo')
            ORDER BY column_name
        """)

        columnas_verificadas = cur.fetchall()
        if columnas_verificadas:
            print("  Columnas verificadas:")
            for col in columnas_verificadas:
                print(f"    - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
        else:
            print("  [WARN] No se encontraron las columnas esperadas")

        # Estadísticas
        print("\n[5/5] Estadísticas de usuarios...")
        cur.execute("SELECT COUNT(*) FROM users")
        total_usuarios = cur.fetchone()[0]
        print(f"  Total de usuarios en el sistema: {total_usuarios}")

        if total_usuarios > 0:
            print(f"\n  [INFO] NOTA: Los {total_usuarios} usuarios existentes necesitaran")
            print("         completar su perfil la proxima vez que inicien sesion")

        print("\n" + "="*60)
        print("[OK] MIGRACION COMPLETADA EXITOSAMENTE")
        print("="*60)

        # Cerrar conexión
        cur.close()
        conn.close()

    except psycopg2.OperationalError as e:
        print(f"\n[ERROR] ERROR DE CONEXION: {e}")
        print("\nVerifica que:")
        print("  1. PostgreSQL este corriendo")
        print("  2. Las credenciales de DB_CONFIG sean correctas")
        print("  3. La base de datos 'abogadai_db' exista")
        return False

    except Exception as e:
        print(f"\n[ERROR] ERROR INESPERADO: {e}")
        return False

    return True


if __name__ == "__main__":
    print("\n")
    print("[WARN] IMPORTANTE: Asegurate de tener un backup de la base de datos antes de continuar")
    print()

    respuesta = input("Deseas continuar con la migracion? (si/no): ").strip().lower()

    if respuesta in ['si', 's', 'yes', 'y']:
        print()
        success = migrate()
        if success:
            print("\n[OK] Migracion completada. Ahora puedes:")
            print("   1. Actualizar el modelo User en app/models/user.py")
            print("   2. Actualizar los schemas en app/schemas/user.py")
            print("   3. Crear el router de perfil en app/routes/perfil.py")
    else:
        print("\n[INFO] Migracion cancelada por el usuario")
