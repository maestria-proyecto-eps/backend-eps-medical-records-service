from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from db.session import get_db_audit
from models.AdminMed import AdminMed
from models.AdminMedItems import AdminMedItems
from models.PrescripcionesItems import PrescripcionesItems
from schemas.Create.AdministracionMedCreate import AdministracionMedCreate
from models.Prescripciones import Prescripciones
from models.AtencionHospitalizacion import AtencionHospitalizacion
from models.Medicamento import Medicamento
from typing import Optional
from datetime import datetime
from core.dependencias import RequireRole
router = APIRouter(prefix="/api", tags=["Administracion medicamentos"], dependencies=[Depends(RequireRole(["Enfermero"]))])

@router.post("/administracion_medicamentos")
def post_admin_med(
        info: AdministracionMedCreate,
        db: Session = Depends(get_db_audit)
):
    try:
        new_admin = AdminMed(
            id_enfermera=info.id_enfermera,
            id_hospitalizacion=info.id_hospitalizacion
        )
        db.add(new_admin)

        db.flush()

        for item_id in info.admin_med_items:
            item_prescripcion = db.query(PrescripcionesItems).join(
                Prescripciones,
                PrescripcionesItems.id_prescripcion == Prescripciones.id_prescripcion
            ).filter(
                PrescripcionesItems.id_items == item_id,
                Prescripciones.tipo == 3
            ).first()

            if not item_prescripcion:
                raise Exception(f"El medicamento con ID {item_id} no está prescrito para hospitalización.")

            nuevo_detalle = AdminMedItems(
                id_admin_med=new_admin.id_admin_med,
                id_items=item_id,
                id_prescripcion_items=item_prescripcion.id_items
            )
            db.add(nuevo_detalle)


        db.commit()
        db.refresh(new_admin)

        return {
            "hasError": False,
            "Message": "tabla exitoso",
            "Data": {"admin_med": new_admin,"admin_med_items": nuevo_detalle}
    }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en la transacción: {str(e)}"
        )

@router.get("/prescriptions/items/hospitalizacion/{id_hospitalizacion}")
def get_prescripciones_hospitalizacion(
        id_hospitalizacion: int,
        id_medicamento: int = Query(None),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db_audit)
):
    try:

        query = db.query(PrescripcionesItems).options(
            joinedload(PrescripcionesItems.medicamento)
        ).join(
            Prescripciones,
            PrescripcionesItems.id_prescripcion == Prescripciones.id_prescripcion
        ).join(
            AtencionHospitalizacion,
            Prescripciones.id_atencion == AtencionHospitalizacion.id_atencionh
        ).filter(
            AtencionHospitalizacion.id_hospitalizacion == id_hospitalizacion,
            Prescripciones.tipo == 3
        )


        if id_medicamento:
            query = query.filter(PrescripcionesItems.id_medicamento == id_medicamento)


        total_items = query.count()
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()

        return {
            "hasError": False,
            "Message": "Consulta exitosa",
            "Data": items,
            "Pagination": {
                "TotalItems": total_items,
                "Page": page,
                "PageSize": page_size
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al consultar: {str(e)}")



@router.get("/administracion_medicamentos/{id_hospitalizacion}")
def get_admin_med_por_hospitalizacion(
        id_hospitalizacion: int,
        id_enfermera: Optional[int] = Query(None, description="Filtro opcional por ID de la enfermera"),
        fecha_inicio: Optional[datetime] = Query(None, description="Filtro inicio rango fecha_admin (YYYY-MM-DDTHH:MM:SS)"),
        fecha_fin: Optional[datetime] = Query(None, description="Filtro fin rango fecha_admin (YYYY-MM-DDTHH:MM:SS)"),
        db: Session = Depends(get_db_audit)
):
    try:

        query = db.query(
            AdminMed, AdminMedItems, PrescripcionesItems, Medicamento
        ).join(
            AdminMedItems, AdminMed.id_admin_med == AdminMedItems.id_admin_med
        ).join(
            PrescripcionesItems, AdminMedItems.id_items == PrescripcionesItems.id_items
        ).join(
            Medicamento, PrescripcionesItems.id_medicamento == Medicamento.codigo
        ).filter(
            AdminMed.id_hospitalizacion == id_hospitalizacion
        )


        if id_enfermera is not None:
            query = query.filter(AdminMed.id_enfermera == id_enfermera)

        if fecha_inicio is not None:
            query = query.filter(AdminMed.fecha_admin >= fecha_inicio)

        if fecha_fin is not None:
            query = query.filter(AdminMed.fecha_admin <= fecha_fin)


        resultados = query.all()


        administraciones_dict = {}

        for admin, admin_item, presc_item, medicamento in resultados:
            if admin.id_admin_med not in administraciones_dict:
                administraciones_dict[admin.id_admin_med] = {
                    "id_admin_med": admin.id_admin_med,
                    "id_enfermera": admin.id_enfermera,
                    "fecha_admin": admin.fecha_admin,
                    "id_hospitalizacion": admin.id_hospitalizacion,
                    "items_administrados": []
                }


            administraciones_dict[admin.id_admin_med]["items_administrados"].append({
                "admin_item_detalle": admin_item,
                "prescripcion_item": presc_item,
                "medicamento": medicamento
            })


        data_respuesta = list(administraciones_dict.values())

        return {
            "hasError": False,
            "Message": "Consulta exitosa",
            "Data": data_respuesta
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los registros: {str(e)}"
        )

