# Simulamos un "repository.py"
class Repository:
    @staticmethod
    def buscar_dato():
        return "dato real de la base de datos"

# Simulamos un "service.py" que importa y usa el repository
def obtener_dato_service():
    return Repository.buscar_dato()

from unittest.mock import patch

def test_obtener_dato_con_mock():
    with patch(__name__ + ".Repository") as mock_repo:
        mock_repo.buscar_dato.return_value = "dato falso"
        resultado = obtener_dato_service()
        assert resultado == "dato falso"