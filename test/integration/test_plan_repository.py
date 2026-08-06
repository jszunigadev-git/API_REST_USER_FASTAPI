import pytest
import psycopg2
from repository import PlanRepository


def test_exclude_constraint_rechaza_solape_de_planes(db_cursor):
    # Setup: usuario y membresía de prueba
    db_cursor.execute("""
        INSERT INTO usuario (id, nombre, email, telefono)
        VALUES (9001, 'Usuario Test', 'test@test.com', '123456')
    """)
    db_cursor.execute("""
        INSERT INTO membresia (id, nombre, precio, duracion_meses)
        VALUES (9001, 'Membresia Test', 10000, 1)
    """)

    # Primer plan: válido, del 1 al 31 de agosto
    db_cursor.execute("""
        INSERT INTO plan (usuario_id, membresia_id, fecha_inicio, fecha_fin, estado)
        VALUES (9001, 9001, '2026-08-01', '2026-08-31', 'activo')
    """)

    # Segundo plan: se solapa con el primero (empieza el 15 de agosto, dentro del rango)
    with pytest.raises(psycopg2.errors.ExclusionViolation):
        db_cursor.execute("""
            INSERT INTO plan (usuario_id, membresia_id, fecha_inicio, fecha_fin, estado)
            VALUES (9001, 9001, '2026-08-15', '2026-09-15', 'activo')
        """)
        
@pytest.fixture
def plan_dict():
    return {
      "fecha_inicio" : '2026-08-01',
      "fecha_fin" : '2026-08-31',
      "estado" : 'activo'
    }

@pytest.mark.parametrize("obtener_funcion,key_id,es_lista",[
    (PlanRepository.obtener_planes,None,True),
    (PlanRepository.obtener_plan_id,"id",False),
    (PlanRepository.obtener_plan_usuario,"usuario_id",True),
    (PlanRepository.obtener_plan_vigente_por_usuario,"usuario_id",True),
])
def test_plan_select_by(setup_plan, plan_dict, obtener_funcion, key_id, es_lista):
    
    plan_dict.update(**setup_plan)
    
    plan_id = PlanRepository.crear_plan(plan_dict)
    
    assert plan_id is not None
    
    plan_dict["id"] = plan_id
    
    if key_id:
        target_id = plan_dict[key_id]
        resultado = obtener_funcion(target_id)
    else:
        resultado = obtener_funcion()
    
    if es_lista:
      assert isinstance(resultado, list)
      assert len(resultado) > 0
      id_buscado = [p["id"] for p in resultado]
      assert plan_id in id_buscado
    
    else:
       assert isinstance(resultado, dict)
       assert resultado["id"] == plan_id
    
    
def test_plan_vigente_entre_fecha_por_usuario(setup_plan, plan_dict):
    
    plan_dict.update(**setup_plan)
    
    plan_id = PlanRepository.crear_plan(plan_dict)
    
    assert plan_id is not None
    
    usuario_id = setup_plan["usuario_id"]
    fecha_inicio = '2026-08-01'
    fecha_fin =  '2026-08-31'

    resultado = PlanRepository.obtener_plan_vigente_entre_fecha_por_usuario(usuario_id, fecha_inicio, fecha_fin)

    assert isinstance(resultado, bool)
    assert resultado is True


def test_plan_actualizar_plan(setup_plan, plan_dict):
    
    plan_dict.update(**setup_plan)
    
    plan_id = PlanRepository.crear_plan(plan_dict)
    
    assert plan_id is not None
    
    plan_dict["estado"] = "cancelado"
    
    resultado = PlanRepository.actualizar_plan(plan_id, plan_dict)

    assert isinstance(resultado, bool)
    assert resultado is True
    
    verificacion = PlanRepository.obtener_plan_id(plan_id)
    
    assert verificacion["estado"] == "cancelado"

    
        