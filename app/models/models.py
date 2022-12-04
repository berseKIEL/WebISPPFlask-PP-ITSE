from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

# Reciclaje de codigo
'''
try:
    cur = mysql.connection.cursor()
    consulta = ("select * from y where x = %s")
    cur.execute(consulta, [(query)])
    return cur.fetchone()
except Exception as ex:
    print(ex)
    raise Exception(ex)
'''


class Usuario(UserMixin):
    def __init__(self, id=None, usuario=None, usuariocorreo=None, usuariocontraseña=None, usuariocontraseñatemp=False, usuarioestado=0):
        self.id = id
        self.usuario = usuario
        self.usuariocorreo = usuariocorreo
        self.usuariocontraseña = usuariocontraseña
        self.usuariocontraseñatemp = usuariocontraseñatemp
        self.usuarioestado = usuarioestado

    @classmethod
    def create_user(self, db, dni):
        try:
            cur = db.connection.cursor()
            consulta = (
                'INSERT INTO usuario(usuario,usuariocontraseñatemp) VALUES(%s,%s)')
            cur.execute(consulta, [dni, dni])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuario_DNI(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select * from usuario where usuario = %s")
            cur.execute(consulta, [(user.usuario)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuario_id(self, mysql, iduser):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select * from usuario where usuarioid = %s")
            cur.execute(consulta, [(iduser)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuario_email(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select * from usuario where usuariocorreo = %s")
            cur.execute(consulta, [(user.usuariocorreo)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuario_correo(self, mysql, correo):
        try:
            cur = mysql.connection.cursor()
            consulta = (
                "select usuariocorreo from usuario where usuariocorreo = %s")
            cur.execute(consulta, [(correo)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def return_queried_user(self, mysql, user):
        try:
            row = Usuario.get_usuario_DNI(mysql, user)
            if row != None:
                temp = row[4]
                if row[5] == 0:
                    if str(temp) == str(user.usuariocontraseña):
                        temp = True
                        user = Usuario(row[0], row[1], row[2],
                                       row[3], temp, row[5])
                    else:
                        temp = False
                        user = Usuario(row[0], row[1], row[2],
                                       row[3], temp, row[5])
                    return user
                else:
                    if temp != None:
                        temp = True
                        user = Usuario(row[0], row[1], row[2],
                                       row[3], temp, row[5])
                    else:
                        temp = False
                        user = Usuario(row[0], row[1], row[2], Usuario.revisar_contraseña_hasheada(
                            row[3], user.usuariocontraseña), temp, row[5])
                    return user
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_temp_password(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET UsuarioContraseñaTemp = NULL WHERE usuarioid = %s')
            cur.execute(consulta, [str(id)])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_temp_password_password(self, db, newpassword, correo):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET UsuarioContraseñaTemp = %s WHERE usuariocorreo = %s')
            cur.execute(consulta, [(newpassword), str(correo)])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_password(self, db, password, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET usuariocontraseña = %s WHERE usuarioid = %s')
            cur.execute(
                consulta, [Usuario.generar_contraseña_hasheada(password), id])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def resetear_contraseña(self, db, usuarioid):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET usuariocontraseñatemp = (select usuario from usuario where usuarioid = %s),usuariocontraseña = NULL, usuariocorreo = NULL, usuarioactivo = 0 WHERE usuarioid = %s')
            cur.execute(consulta, [usuarioid, usuarioid])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_email(self, db, email, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET usuariocorreo = %s WHERE usuarioid = %s')
            cur.execute(consulta, [email, id])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def activate_user(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET usuarioactivo = 1 WHERE usuarioid = %s')
            cur.execute(consulta, [(id)])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def deactivate_user(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET usuarioactivo = 0 WHERE usuarioid = %s')
            cur.execute(consulta, [(id)])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def revisar_contraseña_hasheada(self, hash, contraseña):
        return check_password_hash(hash, contraseña)

    @classmethod
    def generar_contraseña_hasheada(self, contraseña):
        return generate_password_hash(contraseña)

    @classmethod
    def get_login_id(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = ("select * from usuario where usuarioid = %s")
            cur.execute(consulta, [(id)])
            row = cur.fetchone()
            if row != None:
                user = Usuario(row[0], row[1], row[2], row[3], row[4], row[5])
                return user
            else:
                return None

        except Exception as ex:
            print(ex)
            raise Exception(ex)


class Perfil():
    def __init__(self, id=None, perfil=None):
        self.id = id
        self.perfil = perfil

    @classmethod
    def get_all_perfiles(self, db):
        try:
            cur = db.connection.cursor()
            consulta = ("select * from perfil")
            cur.execute(consulta)
            return cur.fetchall()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_perfil_via_id(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = ("select * from perfil where perfilid = %s")
            cur.execute(consulta, [id])
            return cur.fetchall()
        except Exception as ex:
            print(ex)
            raise Exception(ex)


class UsuarioPerfil():
    def __init__(self, id=None, perfilid=None, usuarioid=None, usuarioperfilactivo=0):
        self.id = id
        self.perfilid = perfilid
        self.usuarioid = usuarioid
        self.usuarioperfilactivo = usuarioperfilactivo

    @classmethod
    def create_userperfil(self, db, usuarioid, perfilid):
        try:
            cur = db.connection.cursor()
            consulta = (
                'INSERT INTO usuarioperfil(perfilid, usuarioid) VALUES(%s,%s)')
            cur.execute(consulta, [int(perfilid), int(usuarioid)])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuarioperfilid(self, db, usuarioid, perfilid):
        try:
            cur = db.connection.cursor()
            consulta = (
                "select usuarioperfilid from usuarioperfil where usuarioid = %s and perfilid = %s")
            cur.execute(consulta, [usuarioid, perfilid])
            return cur.fetchone()[0]
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuarioperfil_via_user_activo(self, db, usuarioid, perfilid):
        try:
            cur = db.connection.cursor()
            consulta = (
                "select usuarioperfilactivo from usuarioperfil where usuarioid = %s and perfilid = %s")
            cur.execute(consulta, [usuarioid, perfilid])
            return cur.fetchone()[0]
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_perfilid_via_userid(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                "select perfilid from usuarioperfil where usuarioid = %s")
            cur.execute(consulta, [id])
            return cur.fetchall()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_count_usuarioperfil(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'select COUNT(UsuarioPerfilID) from usuarioperfil where usuarioid = %s')
            cur.execute(consulta, [id])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def activate_user_perfil(self, db, id, perfilid):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuarioperfil SET usuarioperfilactivo = 1 WHERE usuarioid = %s AND perfilid = %s')
            cur.execute(consulta, [id, perfilid])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def deactivate_user_perfil(self, db, id, perfilid):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuarioperfil SET usuarioperfilactivo = 0 WHERE usuarioid = %s AND perfilid = %s')
            cur.execute(consulta, [id, perfilid])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuarioid_from_usuarioperfil(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                "select usuarioid from usuarioperfil where usuarioperfilid = %s")
            cur.execute(consulta, [id])
            usuarios = []
            usuarios.append(cur.fetchone()[0])
            usuarios.append(id)
            return usuarios
        except Exception as ex:
            print(ex)
            raise Exception(ex)


class usuarioDatos():
    def __init__(self, UsuarioID, UsuarioNombre, UsuarioApellido, UsuarioCUIL, UsuarioFechaNac, UsuarioSexoDNI) -> None:
        self.UsuarioID = UsuarioID
        self.UsuarioNombre = UsuarioNombre
        self.UsuarioApellido = UsuarioApellido
        self.UsuarioCUIL = UsuarioCUIL
        self.UsuarioFechaNac = UsuarioFechaNac
        self.UsuarioSexoDNI = UsuarioSexoDNI

    @classmethod
    def get_usuario_datos_id(self, mysql, id):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select * from usuariodatos where usuarioid = %s")
            cur.execute(consulta, [(id)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_cuilfnac_id(self, mysql, id):
        try:
            cur = mysql.connection.cursor()
            consulta = (
                "select usuariocuil, usuariofechanac from usuariodatos where usuarioid = %s")
            cur.execute(consulta, [(id)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_Nombre_Apellido_from_usuariodatos(self, mysql, usuarioid):
        try:
            cur = mysql.connection.cursor()
            consulta = (
                'SELECT UsuarioNombre, UsuarioApellido, observaciones FROM usuariodatos WHERE usuarioid = %s')
            cur.execute(consulta, [usuarioid])
            NombreApellido = cur.fetchone()
            # usuarioPerfilesid = cur.fetchall()
            return NombreApellido
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def insert_usuariodatos(self, db, usuarioid, UsuarioNombre, UsuarioApellido, observaciones):
        try:
            cur = db.connection.cursor()
            consulta = (
                'INSERT INTO usuariodatos(usuarioid, UsuarioNombre,UsuarioApellido, observaciones) VALUES(%s,%s,%s,%s)')

            cur.execute(consulta, [usuarioid, UsuarioNombre,
                        UsuarioApellido, observaciones])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)


class personal():
    def __init__(self, personalid, usuarioperfilid) -> None:

        self.personalid = personalid
        self.usuarioperfilid = usuarioperfilid

    @classmethod
    def get_personalid(self, mysql, usuarioperfilid):
        try:
            cur = mysql.connection.cursor()
            consulta = (
                "SELECT personalid FROM personal WHERE usuarioperfilid = %s")
            cur.execute(consulta, [int(usuarioperfilid)])
            return cur.fetchone()[0]
        except Exception as ex:
            print(ex)
            raise Exception(ex)


class alumno():
    def __init__(self, alumnoid, usuarioperfilid) -> None:

        self.alumnolid = alumnoid
        self.usuarioperfilid = usuarioperfilid

    @classmethod
    def get_usuarioperfil_from_alumno(self, mysql, alumnoid):
        try:
            cur = mysql.connection.cursor()
            consulta = (
                'SELECT usuarioperfilid FROM alumno WHERE alumnoid = %s')
            cur.execute(consulta, [alumnoid])
            usuarioperfilesid = cur.fetchone()[0]
            # usuarioPerfilesid = cur.fetchall()
            return usuarioperfilesid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_alumnoid_by_usuarioperfilid(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                "select alumnoid from alumno where usuarioperfilid = %s")
            cur.execute(consulta, [id])
            return cur.fetchone()[0]
        except Exception as ex:
            print(ex)
            raise Exception(ex)


class Carpo():
    def __init__(self, carpoid, carreraid, plandeestudioid, orientacionid, carpoprograma, estado) -> None:
        self.carpoid = carpoid
        self.carreraid = carreraid
        self.plandeestudioid = plandeestudioid
        self.orientacionid = orientacionid
        self.carpoprograma = carpoprograma
        self.estado = estado

    @classmethod
    def get_carpo_nombres(self, mysql):
        try:
            cur = mysql.connection.cursor()
            consulta = ("SELECT carpoid, carreranombre, OrientacionID, plannombre FROM (carpo as c inner join carrera as car on c.CarreraID = car.carreraid) inner join plandeestudio as p on c.plandeestudioid = p.PlanID order by CARPOID")
            cur.execute(consulta)
            carpo = cur.fetchall()
            carpo2 = []
            for i in range(len(carpo)):

                if carpo[i][2] != None:
                    consulta = 'SELECT orientacionnombre FROM orientacion WHERE orientacionid = %s'
                    cur.execute(consulta, [carpo[i][2]])
                    list = [carpo[i][0], carpo[i][1],
                            cur.fetchone()[0], carpo[i][3]]
                    carpo2.append(list)
                else:
                    carpo2.append(carpo[i])
            return carpo2
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_carpo_nombres_from_id(self, mysql, carpoid):
        try:
            cur = mysql.connection.cursor()
            consulta = ("SELECT carpoid, carreranombre, OrientacionID, plannombre FROM (carpo as c inner join carrera as car on c.CarreraID = car.carreraid) inner join plandeestudio as p on c.plandeestudioid = p.PlanID WHERE CARPOID = %s")
            cur.execute(consulta, [carpoid])
            carpo = cur.fetchall()
            carpo2 = []
            for i in range(len(carpo)):

                if carpo[i][2] != None:
                    consulta = 'SELECT orientacionnombre FROM orientacion WHERE orientacionid = %s'
                    cur.execute(consulta, [carpo[i][2]])
                    list = [carpo[i][0], carpo[i][1],
                            cur.fetchone()[0], carpo[i][3]]
                    carpo2.append(list)
                else:
                    carpo2.append(carpo[i])

            return carpo2[0]
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_carpo_ids(self, mysql, carpoid):
        try:
            cur = mysql.connection.cursor()
            consulta = (
                "SELECT carreraid, orientacionid, plandeestudioid FROM carpo WHERE carpoid = %s")
            cur.execute(consulta, [carpoid])
            carpo = cur.fetchone()
            return carpo
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_result_ori(self, mysql, carreraid):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT orientacion.OrientacionID,orientacion.OrientacionNombre FROM carrera JOIN carpo ON carrera.carreraID= carpo.carreraID JOIN orientacion ON orientacion.OrientacionID = carpo.OrientacionID WHERE carrera.carreraID=%s'
            cur.execute(sql, [carreraid])
            ori = cur.fetchall()
            if len(ori) == 0:
                ori = None
            return ori
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def search_carpo(self, mysql, CarreraID,OrientacionID,PlanID):
        try:
            cur=mysql.connection.cursor()
            if OrientacionID<1:
                sql='SELECT carpoid FROM carpo WHERE carreraid = %s AND plandeestudioid = %s'
                cur.execute(sql,[CarreraID,PlanID])
            else:
                sql = 'Select carpoid from carpo where carreraid = %s and plandeestudioid = %s and OrientacionID = %s'
                cur.execute(sql,[CarreraID,PlanID,OrientacionID])
            CarpoID = cur.fetchone()
            return CarpoID[0]
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def name_carpo(self,mysql,CarpoID):
        try:
            cur=mysql.connection.cursor()
            sql="SELECT CarreraNombre, OrientacionNombre, PlanNombre FROM (((carpo AS C left join carrera AS car ON C.CarreraID = car.CarreraID) inner join plandeestudio AS P ON C.PlanDeEstudioID = P.PlanID) LEFT join orientacion AS ori ON C.OrientacionID = ori.OrientacionID) WHERE C.CARPOID = %s;"
            cur.execute(sql,[CarpoID])
            nombre = cur.fetchone()
            return nombre 

        except Exception as ex:
            raise Exception(ex)

class Plan():
    def __init__(self, PlanID, PlanNombre) -> None:
        self.PlanID = PlanID
        self.PlanNombre = PlanNombre

    @classmethod
    def add_Plan(self, mysql, PlanNombre):
        try:
            cur = mysql.connection.cursor()
            sql = 'INSERT INTO plandeestudio(PlanNombre) VALUES (%s)'
            cur.execute(sql, [PlanNombre])
            mysql.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_Plan_all(self, mysql):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT * FROM plandeestudio'
            cur.execute(sql)
            Plan = cur.fetchall()
            return Plan
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_Plan_id(self, mysql, PlanID):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT * from plandeestudio WHERE PlanID=%s'
            cur.execute(sql, [PlanID])
            Plan = cur.fetchone()
            if Plan:
                return Plan
            else:
                return "vacio"

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit_Plan(self, mysql, PlanID, PlanNombre):
        try:
            cur = mysql.connection.cursor()
            sql = 'UPDATE plandeestudio SET PlanNombre = %s WHERE PlanID = %s'
            cur.execute(sql, [PlanNombre, PlanID])
            mysql.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_Plan(self, mysql, PlanID):
        try:
            cur = mysql.connection.cursor()
            sql = 'delete from plandeestudio where PlanID = %s'
            cur.execute(sql, ([int(PlanID)]))
            mysql.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_plan_via_oricar(self, mysql, carreraid, orientacionid):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT p.PlanID,p.PlanNombre, carpo.CARPOID FROM plandeestudio p JOIN carpo ON p.PlanID = carpo.PlanDeEstudioID WHERE carreraID = %s AND orientacionID = %s'
            cur.execute(sql, [carreraid, orientacionid])
            ori = cur.fetchall()
            return ori
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_plan_via_car(self, mysql, carreraid):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT p.PlanID,p.PlanNombre, carpo.CARPOID FROM plandeestudio p JOIN carpo ON p.PlanID = carpo.PlanDeEstudioID WHERE carreraID = %s'
            cur.execute(sql, [carreraid])
            planes = cur.fetchall()
            return planes
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_nombre_ori_plan(self, mysql, car, ori):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT carreranombre from carrera WHERE carreraid=%s'
            cur.execute(sql, [car])
            car = cur.fetchone()

            nombre = car[0] + '/'

            sql = 'SELECT orientacionnombre from orientacion WHERE orientacionid=%s'
            cur.execute(sql, [ori])
            ori = cur.fetchone()
            if ori != None:
                nombre = nombre + ori[0] + '/'
            return nombre
        except Exception as ex:
            raise Exception(ex)


class Carrera():
    def __init__(self, CarreraID, CarreraNombre) -> None:
        self.CarreraID = CarreraID
        self.CarreraNombre = CarreraNombre

    @classmethod
    def add_Carrera(self, mysql, CarreraNombre):
        try:
            cur = mysql.connection.cursor()
            sql = 'INSERT INTO Carrera(CarreraNombre) VALUES (%s)'
            cur.execute(sql, [CarreraNombre])
            mysql.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_Carrera_all(self, mysql):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT * FROM Carrera'
            cur.execute(sql)
            Carrera = cur.fetchall()
            return Carrera
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_Carrera_id(self, mysql, CarreraID):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT * from Carrera WHERE CarreraID=%s'
            cur.execute(sql, [CarreraID])
            Carrera = cur.fetchone()
            if Carrera:
                return Carrera
            else:
                return "vacio"

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit_Carrera(self, mysql, CarreraID, CarreraNombre):
        try:
            cur = mysql.connection.cursor()
            sql = 'UPDATE Carrera SET CarreraNombre = %s WHERE CarreraID = %s'
            cur.execute(sql, [CarreraNombre, CarreraID])
            mysql.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_Carrera(self, mysql, CarreraID):
        try:
            cur = mysql.connection.cursor()
            sql = 'delete from Carrera where CarreraID = %s'
            cur.execute(sql, ([int(CarreraID)]))
            mysql.connection.commit()
        except Exception as ex:
            raise Exception(ex)

class Materia():
    def __init__(self, MateriaID, MateriaNombre, MateriaAño, MateriaTipo, CarpoIDMat) -> None:
        self.MateriaID = MateriaID
        self.MateriaNombre = MateriaNombre
        self.MateriaAño = MateriaAño
        self.MateriaTipo = MateriaTipo
        self.CarpoIDMat = CarpoIDMat

    @classmethod
    def add_Materia(self, mysql, MateriaNombre, MateriaAño, MateriaTipo, CarpoIDMat):
        try:
            cur = mysql.connection.cursor()
            sql = 'INSERT INTO Materia(MateriaNombre, MateriaAño, MateriaTipo,CarpoIDMat) VALUES (%s, %s, %s,%s)'
            cur.execute(sql, [MateriaNombre, MateriaAño, MateriaTipo, CarpoIDMat])
            mysql.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_Materia_all(self, mysql, CarpoIDMat):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT materiaid,MateriaNombre, Materiaaño, materiatipo FROM Materia where CarpoIDMat = %s ORDER BY MateriaTipo ASC'
            cur.execute(sql,[CarpoIDMat])
            Materia = cur.fetchall()
            return Materia
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_Materia_id(self, mysql, MateriaID):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT * from Materia WHERE MateriaID=%s'
            cur.execute(sql, [MateriaID])
            Materia = cur.fetchone()
            if Materia:
                return Materia
            else:
                return "vacio"

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def edit_Materia(self, mysql, MateriaID, MateriaNombre, MateriaAño, MateriaTipo):
        try:
            cur = mysql.connection.cursor()
            sql = 'UPDATE Materia SET MateriaNombre = %s, MateriaAño = %s, MateriaTipo = %s WHERE MateriaID = %s'
            cur.execute(sql, [MateriaNombre, MateriaAño,
                        MateriaTipo, MateriaID])
            mysql.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_Materia(self, mysql, MateriaID):
        try:
            cur = mysql.connection.cursor()
            sql = 'delete from Materia where MateriaID = %s'
            cur.execute(sql, ([int(MateriaID)]))
            mysql.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def cantidadDeAños(self, mysql,idcarpo):
        try:
            cur = mysql.connection.cursor()
            sql='SELECT COUNT(DISTINCT(m.MateriaAño)) FROM carpo c JOIN materia m ON c.CARPOID = m.carpoidmat WHERE CARPOID = %s'            
            cur.execute(sql,[idcarpo])
            año = cur.fetchone()
            año=año[0]
            return año
        except Exception as ex:
            raise Exception(ex)

class personalcarpo():
    def __init__(self, personalcarpoid, personalid, carpoid, personalcarpoactivo) -> None:
        self.personalcarpoid = personalcarpoid
        self.personalid = personalid
        self.carpoid = carpoid
        self.personalcarpoactivo = personalcarpoactivo

    @classmethod
    def cargar_personalcarpo(self, mysql, personalid, carpoid):
        try:
            cur = mysql.connection.cursor()
            consulta = (
                "INSERT INTO personalcarpo(personalid, carpoid) VALUES(%s,%s)")
            cur.execute(consulta, [personalid, carpoid])
            mysql.connection.commit()

            return True
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def eliminar_personalcarpo(self, mysql, personalid, carpoid):
        try:
            cur = mysql.connection.cursor()
            consulta = (
                "DELETE FROM personalcarpo WHERE CarpoID = %s and personalid = %s")
            cur.execute(consulta, [carpoid, personalid])
            mysql.connection.commit()

            return True
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def cantcarpo(self, mysql, personalid):
        try:
            cur = mysql.connection.cursor()
            consulta = (
                "SELECT carpoid FROM personalcarpo where personalid = %s")
            cur.execute(consulta, [personalid])
            return cur.fetchall()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

class alumnocarpo():
    def __init__(self, alumnocarpoid, carpoid, alumnoid, alumnocarpoactivo) -> None:

        self.alumnocarpolid = alumnocarpoid
        self.carpoid = carpoid
        self.alumnoid = alumnoid
        self.alumnocarpoactivo = alumnocarpoactivo

    @classmethod
    def insert_alumnocarpo(self, db, alumnoid, carpoid):
        try:
            cur = db.connection.cursor()
            consulta = (
                'INSERT INTO alumnocarpo(alumnoid,carpoid) VALUES(%s,%s)')
            cur.execute(consulta, [alumnoid, carpoid])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_alumno_from_alumnocarpo(self, mysql, carpoid):
        try:
            cur = mysql.connection.cursor()
            consulta = ("SELECT alumnoid FROM alumnocarpo WHERE carpoid = %s")
            cur.execute(consulta, [int(carpoid)])
            alumnos = cur.fetchall()
            return alumnos
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_carpoid_by_alumnoid(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                "select carpoid from alumnocarpo where alumnoid = %s")
            cur.execute(consulta, [id])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)
