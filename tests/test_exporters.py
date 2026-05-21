import pytest
from src.exporters import write_sif, write_summary

def test_write_sif_writes_expected_labels(tmp_path):
    interactions = [
        ("CRP", "lacZ", "+"),
        ("FNR", "narG", "-"),
        ("AraC", "araB", "+-"),
    ]
    out_file = tmp_path / "network.sif"
    write_sif(interactions, out_file)
    content = out_file.read_text()
    assert "CRP\tactivates\tlacZ" in content
    assert "FNR\trepresses\tnarG" in content
    assert "AraC\tregulates\taraB" in content

def test_write_summary_escibe_cabecera_y_datos(tmp_path):
    regulon = {
        "CRP": {
            "genes": ["lacZ", "araB"],
            "activados": 2,
            "reprimidos": 0,
        }
    }
    out_file = tmp_path / "summary.tsv"
    write_summary(regulon, out_file)
    content = out_file.read_text()
    assert "TF\tTotal genes\tActivados\tReprimidos\tTipo\tLista de genes" in content
    assert "CRP" in content
    assert "2\t2\t0\tactivador" in content
    assert "lacZ, araB" in content or "araB, lacZ" in content  # orden puede variar

def test_write_summary_lanza_error_si_regulon_es_none(tmp_path):
    with pytest.raises(ValueError):  # o el tipo de error que tu función lance
        write_summary(None, tmp_path / "out.tsv")

def test_write_sif_lanza_error_si_archivo_salida_esta_vacio(tmp_path):
    with pytest.raises(ValueError):
        write_sif([("CRP", "lacZ", "+")], "")