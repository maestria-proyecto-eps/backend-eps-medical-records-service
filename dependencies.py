#Repositories
from fastapi.params import Depends
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from db.session import get_db_audit, get_db_admin_audit
from services.PreinscripcionesService import PreinscripcionesService
from services.CatalogoDiagnosticoService import CatalogoDiagnosticoService
from services.CitaService import CitatService
from services.HistoriaService import HistoriaService
from services.MedicamentoService import MedicamentoService
from services.repositories.CatalogoDiagnosticoRepository import CatalogoDiagnosticoRepository
from services.repositories.CitaRepository import CitaRepository
from services.repositories.HistoriaRepository import HistoriaRepository
from services.repositories.MedicamentoRepository import MedicamentoRepository
from services.repositories.RegistroRepository import RegistroRepository
from services.repositories.PrescripcionesRepository import PrescripcionesRepository
from services.repositories.PrescripcionesItemsRepository import PrescripcionesItemsRepository
from services.repositories.EspecialidadRepository import EspecialidadRepository
from services.repositories.RemisionesRepository import RemisionesRepository
from services.repositories.PersonaRepository import PersonaRepository

#Repositories
def getCitaRepository(db = Depends(get_db_audit))-> CitaRepository:
    return CitaRepository(db)
def getRegistroRepository(db = Depends(get_db_audit))-> RegistroRepository:
    return RegistroRepository(db)
def getHistoriaRepository(db = Depends(get_db_audit))-> HistoriaRepository:
    return HistoriaRepository(db)
def getDiagnosticoRepository(db = Depends(get_db_audit))-> CatalogoDiagnosticoRepository:
    return CatalogoDiagnosticoRepository(db)

def getMedicamentoRepository(db = Depends(get_db_audit))-> MedicamentoRepository:
    return MedicamentoRepository(db)

def getPrescripcionesRepository(db = Depends(get_db_audit))-> PrescripcionesRepository:
    return PrescripcionesRepository(db)

def getPrescripcionesItemsRepository(db = Depends(get_db_audit))-> PrescripcionesItemsRepository:
    return PrescripcionesItemsRepository(db)
def getetEspecialidadRepository(db = Depends(get_db_admin_audit))-> EspecialidadRepository:
    return EspecialidadRepository(db)
def getRemisionesRepository(db = Depends(get_db_audit))-> RemisionesRepository:
    return RemisionesRepository(db)

def getUsuarioRepository(db = Depends(get_db_admin_audit))-> PersonaRepository:
    return PersonaRepository(db)

#Services
def getCitaService(citaRepository = Depends(getCitaRepository), 
                   registroRepository = Depends(getRegistroRepository),
                   diagnosticoRepository = Depends(getDiagnosticoRepository),
                   medicamentoRepository = Depends(getMedicamentoRepository),
                   prescripcionesRepository = Depends(getPrescripcionesRepository),
                   prescripcionesItemsRepository = Depends(getPrescripcionesItemsRepository),
                   historiaRepository = Depends(getHistoriaRepository),
                   especialidadRepository = Depends(getetEspecialidadRepository),
                   remisionesRepository = Depends(getRemisionesRepository),
                   repositoryPersona = Depends(getUsuarioRepository)) -> CitatService:
    return CitatService(citaRepository, registroRepository, diagnosticoRepository, 
                       medicamentoRepository, prescripcionesRepository, 
                       prescripcionesItemsRepository, historiaRepository,
                       especialidadRepository, remisionesRepository,
                       repositoryPersona)
def getHistoriaService(historiaRepository = Depends(getHistoriaRepository)):
    return HistoriaService(historiaRepository)
def getDiagnosticoService(diagnosticoRepository = Depends(getDiagnosticoRepository)):
    return CatalogoDiagnosticoService(diagnosticoRepository)
def getMedicamentoService(medicamentoRepository = Depends(getMedicamentoRepository)):
    return MedicamentoService(medicamentoRepository)
def getPreinscripcionService(preinscripcionRepository = Depends(getPrescripcionesRepository),
                             medicamentoRepository = Depends(getMedicamentoRepository)):
    return PreinscripcionesService(preinscripcionRepository, medicamentoRepository)


bearer_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials

        payload = jwt.decode(
            token,
            key="",                 # por ahora vacío, NO usamos el secret
            algorithms=["HS256"],
            options={"verify_signature": False}  # clave: solo leemos el payload
        )

        print("JWT payload:", payload)

        user_id = payload.get("id_usuario")
        num_documento = payload.get("num_documento")
        role = payload.get("role")
        role_id = payload.get("id_role")

        if num_documento is None:
            raise credentials_exception

        return {
            "id": user_id,
            "num_documento": num_documento,
            "role": role,
            "role_id": role_id,
            "payload": payload
        }

    except JWTError:
        raise credentials_exception

def get_current_doctor_user(current_user = Depends(get_current_user)):
    role_id = current_user.get("role_id")

    if role_id != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario no autorizado como doctor"
        )
    return current_user


def get_current_patient_user(current_user = Depends(get_current_user)):
    role_id = current_user.get("role_id")

    if role_id != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario no autorizado como paciente"
        )
    return current_user