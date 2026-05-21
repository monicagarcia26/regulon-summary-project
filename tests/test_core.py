from src.core import get_regulator_type, build_regulon

# ---------- pruebas para get_regulator_type ----------
def test_get_regulator_type_returns_activador():
    data = {
        "genes": ["lacZ", "araB"],
        "activados": 2,
        "reprimidos": 0,
    }
    assert get_regulator_type(data) == "activador"

def test_get_regulator_type_returns_represor():
    data = {
        "genes": ["trpA"],
        "activados": 0,
        "reprimidos": 1,
    }
    assert get_regulator_type(data) == "represor"

def test_get_regulator_type_returns_dual():
    data = {
        "genes": ["lacZ", "galE"],
        "activados": 1,
        "reprimidos": 1,
    }
    assert get_regulator_type(data) == "dual"

# ---------- pruebas para build_regulon ----------
def test_build_regulon_counts_activated_and_repressed_genes():
    interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
        ("FNR", "narG", "-"),
    ]
    regulon = build_regulon(interactions)
    
    assert "CRP" in regulon # debe incluir CRP
    assert len(regulon["CRP"]["genes"]) == 2 # CRP regula 2 genes
    assert regulon["CRP"]["activados"] == 2 # CRP activa 2 genes
    assert regulon["FNR"]["reprimidos"] == 1 # FNR reprime 1 gen

def test_build_regulon_no_duplica_genes():
    # Si un mismo regulador y gen aparece dos veces, no debe duplicarse
    interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "lacZ", "+"),  # duplicado
        ("CRP", "araB", "+"),
    ]
    regulon = build_regulon(interactions)
    # Debe tener solo dos genes únicos
    assert len(regulon["CRP"]["genes"]) == 2
    # El conteo de activados debe ser 2 (no 3)
    assert regulon["CRP"]["activados"] == 2