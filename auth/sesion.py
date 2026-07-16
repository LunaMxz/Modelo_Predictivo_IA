from utils.conexion import obtener_conexion
import bcrypt

# Roles disponibles en el sistema. El primer usuario registrado se vuelve
# "Dueño" automáticamente; todos los que se registren después entran como
# "Trabajador de campo" (el de menor privilegio) hasta que un Dueño los
# suba de rol desde Configuración.
ROLES_DISPONIBLES = ["Dueño", "Trabajador de campo", "Agrónomo"]


# =====================================
# LOGIN
# =====================================

def validar_usuario(correo, password):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    sql = """

        SELECT *

        FROM usuarios

        WHERE correo=%s

        AND activo=1

    """

    cursor.execute(sql, (correo,))

    usuario = cursor.fetchone()

    conexion.close()

    if usuario is None:
        return None

    password_bd = usuario["password"]

    if bcrypt.checkpw(
        password.encode("utf-8"),
        password_bd.encode("utf-8")
    ):
        return usuario

    return None


# =====================================
# REGISTRO
# =====================================

def registrar_usuario(nombre, correo, password):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    # Verificar si el correo ya existe
    cursor.execute(
        "SELECT id FROM usuarios WHERE correo=%s",
        (correo,)
    )

    existe = cursor.fetchone()

    if existe:

        conexion.close()

        return False

    # El primer usuario del sistema se vuelve Dueño; el resto entra
    # como Trabajador de campo hasta que un Dueño le suba el rol.
    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")

    hay_usuarios = cursor.fetchone()["total"] > 0

    rol_asignado = "Trabajador de campo" if hay_usuarios else "Dueño"

    # Encriptar contraseña
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    sql = """

        INSERT INTO usuarios(

            nombre,

            correo,

            password,

            rol

        )

        VALUES(

            %s,

            %s,

            %s,

            %s

        )

    """

    cursor.execute(

        sql,

        (

            nombre,

            correo,

            password_hash,

            rol_asignado

        )

    )

    conexion.commit()

    conexion.close()

    return True


# =====================================
# ADMINISTRACIÓN DE ROLES (solo la usa el Dueño desde Configuración)
# =====================================

def obtener_usuarios():
    """Lista todos los usuarios del sistema para el panel de administración."""

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id, nombre, correo, rol FROM usuarios ORDER BY nombre ASC"
    )

    usuarios = cursor.fetchall()

    conexion.close()

    return usuarios


def actualizar_rol(usuario_id, nuevo_rol):
    """Cambia el rol de un usuario. Devuelve False si el rol no es válido."""

    if nuevo_rol not in ROLES_DISPONIBLES:
        return False

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE usuarios SET rol=%s WHERE id=%s",
        (nuevo_rol, usuario_id)
    )

    conexion.commit()

    conexion.close()

    return True