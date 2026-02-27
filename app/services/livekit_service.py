"""
Servicio de gestión de rooms LiveKit.
Detecta y cierra sesiones de avatar inactivas para evitar costos innecesarios.
"""
import logging
from datetime import datetime

from ..core.config import settings
from ..core.database import SessionLocal
from ..models.caso import Caso, EstadoCaso

logger = logging.getLogger(__name__)

# Tiempo máximo que un room puede estar activo antes de ser cerrado (minutos)
MAX_MINUTOS_SESION_ACTIVA = 30


async def cerrar_rooms_inactivos(max_minutos: int = MAX_MINUTOS_SESION_ACTIVA) -> int:
    """
    Lista todos los rooms activos en LiveKit y cierra los que llevan más
    de max_minutos con fecha_inicio_sesion registrada pero sin finalizar.

    Simli desconecta al avatar tras 240s de idle, pero el room LiveKit queda
    abierto. Esta función elimina esos rooms huérfanos y marca el caso como
    ABANDONADO si sigue en estado TEMPORAL.

    Returns:
        Número de rooms cerrados.
    """
    if not settings.LIVEKIT_API_KEY or not settings.LIVEKIT_API_SECRET:
        logger.warning("[LiveKit] Credenciales no configuradas, omitiendo limpieza")
        return 0

    from livekit import api as lk_api

    cerrados = 0
    db = SessionLocal()

    try:
        async with lk_api.LiveKitAPI(
            settings.LIVEKIT_URL,
            settings.LIVEKIT_API_KEY,
            settings.LIVEKIT_API_SECRET,
        ) as lk:
            resp = await lk.room.list_rooms(lk_api.ListRoomsRequest())
            rooms = resp.rooms

            for room in rooms:
                # Solo procesar rooms de caso (formato caso-{id})
                if not room.name.startswith("caso-"):
                    continue

                try:
                    caso_id = int(room.name.split("-")[1])
                except (IndexError, ValueError):
                    continue

                caso = db.query(Caso).filter(Caso.id == caso_id).first()

                # Si el caso no existe o ya tiene fecha_fin → skip
                if not caso or not caso.fecha_inicio_sesion or caso.fecha_fin_sesion:
                    continue

                minutos_activo = (
                    datetime.utcnow() - caso.fecha_inicio_sesion
                ).total_seconds() / 60

                if minutos_activo < max_minutos:
                    continue

                # Cerrar room en LiveKit
                try:
                    await lk.room.delete_room(
                        lk_api.DeleteRoomRequest(room=room.name)
                    )
                except Exception as e:
                    logger.warning(f"[LiveKit] No se pudo borrar room {room.name}: {e}")

                # Marcar caso como ABANDONADO si sigue activo
                if caso.estado == EstadoCaso.TEMPORAL:
                    caso.estado = EstadoCaso.ABANDONADO
                    caso.fecha_fin_sesion = datetime.utcnow()
                    db.commit()

                cerrados += 1
                logger.info(
                    f"[LiveKit] Room {room.name} cerrado "
                    f"({minutos_activo:.1f} min activo, caso #{caso_id})"
                )

    except Exception as e:
        logger.error(f"[LiveKit] Error en limpieza de rooms inactivos: {e}")
    finally:
        db.close()

    return cerrados
