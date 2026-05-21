import pytest
from src.io_utils import load_interactions

def test_load_interactions_ignores_comments_and_header(tmp_path):
    input_file = tmp_path / "interactions.tsv"
    input_file.write_text(
        "# comentario\n"
        "regulatorId\tregulatorName\tX\tX\tgeneName\teffect\tX\n"
        "id1\tCRP\tX\tX\tlacZ\t+\tX\n"
        "id2\tFNR\tX\tX\tnarG\t-\tX\n"
    )
    interactions = load_interactions(input_file)
    assert interactions == [("CRP", "lacZ", "+"), ("FNR", "narG", "-")]

def test_load_interactions_ignoran_efectos_invalidos(tmp_path):
    input_file = tmp_path / "interactions.tsv"
    input_file.write_text(
        "id1\tCRP\tX\tX\tlacZ\t+\tX\n"
        "id2\tFNR\tX\tX\tnarG\t?\tX\n"   # efecto inválido
        "id3\tAraC\tX\tX\taraB\t+-\tX\n"
    )
    interactions = load_interactions(input_file)
    # Solo se conservan '+' y '-' (y '+-' si tu función lo permite)
    # El documento dice que "? se ignora"
    assert ("CRP", "lacZ", "+") in interactions
    assert ("AraC", "araB", "+-") in interactions
    assert ("FNR", "narG", "?") not in interactions

def test_load_interactions_ignora_lineas_vacias(tmp_path):
    input_file = tmp_path / "interactions.tsv"
    input_file.write_text(
        "id1\tCRP\tX\tX\tlacZ\t+\tX\n"
        "\n"
        "id2\tFNR\tX\tX\tnarG\t-\tX\n"
    )
    interactions = load_interactions(input_file)
    assert len(interactions) == 2

def test_load_interactions_lanza_error_para_archivo_no_existente():
    with pytest.raises(FileNotFoundError):
        load_interactions("nonexistent.tsv")

def test_load_interactions_acepta_efecto_plus_minus(tmp_path):
    # Verificar que el efecto "+-" se conserva (si la función lo permite)
    input_file = tmp_path / "interactions.tsv"
    input_file.write_text(
        "id1\tAraC\tX\tX\taraB\t+-\tX\n"
    )
    interactions = load_interactions(input_file)
    assert ("AraC", "araB", "+-") in interactions