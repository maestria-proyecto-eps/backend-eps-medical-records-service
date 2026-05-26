from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.logger import setup_logging, get_logger
from routers import AppoinmentRouter, DiagnosticoRouter, MedicamentoRouter, PattienRouter, ReferralsRouter, \
    PreinscripcionRouter, AdminMedicamentos
from models.Agenda import Agenda
from models.Cita import Cita
from models.CatalogoDiagnostico import CatalogoDiagnostico
from models.Medicamento import Medicamento
from models.HistoriaClinica import HistoriaClinica
from models.RegistroHistoria import RegistroHistoria
from models.Inventario import Inventario
from models.PrescripcionesItems import PrescripcionesItems
from models.Prescripciones import Prescripciones
from models.Remisiones import Remisiones
from models.Especialidad import Especialidad
from models.Persona import Persona

app = FastAPI(
    title="EPS API Appinments",
    description="EPS management API Appoinments",
    version="0.1"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_logging()

# Logger call example
#logger = get_logger(__name__)

@app.get("/")
def root():
    """Root endpoint"""
    #logger.info("Root endpoint called")
    return {
        "message": "EPS API",
        "features": [
            "EPS management API"
        ],
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def root():
    """health endpoint"""
    return {
        "message": "ok"
    }
app.include_router(AdminMedicamentos.router, prefix="/api")

app.include_router(AppoinmentRouter.router, prefix="/api")
app.include_router(PattienRouter.router, prefix="/api")
app.include_router(DiagnosticoRouter.router, prefix="/api")
app.include_router(MedicamentoRouter.router, prefix="/api")
app.include_router(ReferralsRouter.router, prefix="/api")
app.include_router(PreinscripcionRouter.router, prefix="/api")