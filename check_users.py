"""
Script para consultar usuarios registrados en la base de datos de produccion
"""
from sqlalchemy import create_engine, text
import sys

# URL de la base de datos de produccion en Render
RENDER_DATABASE_URL = "postgresql://abogadai_db_user:zz2U57KjeZbinZqNAwIr2SICUnU68Ezj@dpg-d4stu1chg0os73csqgqg-a.virginia-postgres.render.com/abogadai_db"

print("=" * 80)
print("USUARIOS REGISTRADOS EN LA BASE DE DATOS DE PRODUCCION")
print("=" * 80)
print()

try:
    # Conectar a la base de datos de produccion
    print("Conectando a la base de datos de Render...")
    engine = create_engine(RENDER_DATABASE_URL)

    with engine.connect() as conn:
        print("[OK] Conectado exitosamente\n")

        # Consultar usuarios
        query = text("""
            SELECT
                id,
                email,
                nombre,
                apellido,
                identificacion,
                telefono,
                is_active,
                is_admin,
                perfil_completo,
                nivel_usuario,
                created_at
            FROM users
            ORDER BY created_at DESC
        """)

        result = conn.execute(query)
        users = result.fetchall()

        if not users:
            print("No hay usuarios registrados en la base de datos.\n")
        else:
            print(f"Total de usuarios registrados: {len(users)}\n")
            print("-" * 80)

            for user in users:
                print(f"\nID: {user.id}")
                print(f"Email: {user.email}")
                print(f"Nombre: {user.nombre} {user.apellido}")
                print(f"Identificacion: {user.identificacion if user.identificacion else 'No registrada'}")
                print(f"Telefono: {user.telefono if user.telefono else 'No registrado'}")
                print(f"Estado: {'ACTIVO' if user.is_active else 'INACTIVO'}")
                print(f"Admin: {'SI' if user.is_admin else 'NO'}")
                print(f"Perfil completo: {'SI' if user.perfil_completo else 'NO'}")
                print(f"Nivel: {user.nivel_usuario} ({'FREE' if user.nivel_usuario == 0 else 'BRONCE' if user.nivel_usuario == 1 else 'PLATA' if user.nivel_usuario == 2 else 'ORO'})")
                print(f"Fecha registro: {user.created_at}")
                print("-" * 80)

        # Resumen adicional
        print("\n")
        print("RESUMEN:")
        query_stats = text("""
            SELECT
                COUNT(*) as total,
                COUNT(CASE WHEN is_active = true THEN 1 END) as activos,
                COUNT(CASE WHEN is_admin = true THEN 1 END) as admins,
                COUNT(CASE WHEN perfil_completo = true THEN 1 END) as perfiles_completos,
                COUNT(CASE WHEN nivel_usuario = 0 THEN 1 END) as nivel_free,
                COUNT(CASE WHEN nivel_usuario = 1 THEN 1 END) as nivel_bronce,
                COUNT(CASE WHEN nivel_usuario = 2 THEN 1 END) as nivel_plata,
                COUNT(CASE WHEN nivel_usuario = 3 THEN 1 END) as nivel_oro
            FROM users
        """)

        stats = conn.execute(query_stats).fetchone()
        print(f"  Total usuarios: {stats.total}")
        print(f"  Usuarios activos: {stats.activos}")
        print(f"  Administradores: {stats.admins}")
        print(f"  Perfiles completos: {stats.perfiles_completos}")
        print(f"\n  Niveles:")
        print(f"    - FREE: {stats.nivel_free}")
        print(f"    - BRONCE: {stats.nivel_bronce}")
        print(f"    - PLATA: {stats.nivel_plata}")
        print(f"    - ORO: {stats.nivel_oro}")

    print("\n")
    print("=" * 80)
    print("[OK] CONSULTA COMPLETADA")
    print("=" * 80)
    print()

except Exception as e:
    print()
    print("=" * 80)
    print("[ERROR] ERROR AL CONSULTAR USUARIOS")
    print("=" * 80)
    print()
    print(f"Tipo: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    print()

    import traceback
    print("Detalles del error:")
    traceback.print_exc()
    print()
    sys.exit(1)
