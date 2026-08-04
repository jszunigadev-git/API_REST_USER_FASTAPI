import pytest
from unittest.mock import Mock

# --- Función de ejemplo (simulando algo tipo PlanService) ---
def obtener_usuario_activo(id, repository):
    usuario = repository.buscar_usuario(id)
    if not usuario:
        raise ValueError("Usuario no encontrado")
    return usuario["activo"]


# --- Test 1: caso "no encontrado" ---
def test_usuario_no_encontrado_lanza_error():
    repo_falso = Mock()
    repo_falso.buscar_usuario.return_value = None

    with pytest.raises(ValueError, match="Usuario no encontrado"):
        obtener_usuario_activo(1, repo_falso)


def test_usuario_activo_retorna_true():
    repo_falso = Mock()
    repo_falso.buscar_usuario.return_value = {"activo": True}
    
    # ¿qué va aquí?
    assert obtener_usuario_activo(1, repo_falso)