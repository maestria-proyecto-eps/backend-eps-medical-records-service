#Repositories
from fastapi.params import Depends

from db.session import get_db, get_db_admin
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
def getCitaRepository(db = Depends(get_db))-> CitaRepository:
    return CitaRepository(db)
def getRegistroRepository(db = Depends(get_db))-> RegistroRepository:
    return RegistroRepository(db)
def getHistoriaRepository(db = Depends(get_db))-> HistoriaRepository:
    return HistoriaRepository(db)
def getDiagnosticoRepository(db = Depends(get_db))-> CatalogoDiagnosticoRepository:
    return CatalogoDiagnosticoRepository(db)

def getMedicamentoRepository(db = Depends(get_db))-> MedicamentoRepository:
    return MedicamentoRepository(db)

def getPrescripcionesRepository(db = Depends(get_db))-> PrescripcionesRepository:
    return PrescripcionesRepository(db)

def getPrescripcionesItemsRepository(db = Depends(get_db))-> PrescripcionesItemsRepository:
    return PrescripcionesItemsRepository(db)
def getetEspecialidadRepository(db = Depends(get_db_admin))-> EspecialidadRepository:
    return EspecialidadRepository(db)
def getRemisionesRepository(db = Depends(get_db))-> RemisionesRepository:
    return RemisionesRepository(db)

def getUsuarioRepository(db = Depends(get_db_admin))-> PersonaRepository:
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