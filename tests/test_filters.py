from src.filters import filter_by_min_genes, filter_by_type, filter_interactions_by_regulon

# Datos de ejemplo reutilizables
SAMPLE_REGULON = {
    "CRP": {
        "genes": ["lacZ", "araB"],
        "activados": 2,
        "reprimidos": 0,
    },
    "FNR": {
        "genes": ["narG"],
        "activados": 0,
        "reprimidos": 1,
    },
    "AraC": {
        "genes": ["araB", "araC", "araD"],
        "activados": 3,
        "reprimidos": 0,
    },
}

def test_filter_by_min_genes_keeps_only_reguladores_con_suficientes_genes():
    filtered = filter_by_min_genes(SAMPLE_REGULON, min_genes=2)
    assert "CRP" in filtered
    assert "AraC" in filtered
    assert "FNR" not in filtered
    assert len(filtered) == 2

def test_filter_by_type_return_activadores():
    filtered = filter_by_type(SAMPLE_REGULON, regulator_type="activador")
    assert "CRP" in filtered
    assert "AraC" in filtered
    assert "FNR" not in filtered

def test_filter_by_type_returns_represores():
    filtered = filter_by_type(SAMPLE_REGULON, regulator_type="represor")
    assert "FNR" in filtered
    assert "CRP" not in filtered
    assert "AraC" not in filtered

def test_filter_by_type_return_dual():
    # Como no hay dual en SAMPLE_REGULON, debe dar vacío
    filtered = filter_by_type(SAMPLE_REGULON, regulator_type="dual")
    assert len(filtered) == 0

def test_filter_by_type_cuando_no_se_especifica_tipo():
    filtered = filter_by_type(SAMPLE_REGULON, regulator_type=None)
    assert len(filtered) == 3  # todos

def test_filter_interactions_by_regulon():
    # Interacciones originales
    all_interactions = [
        ("CRP", "lacZ", "+"),
        ("CRP", "araB", "+"),
        ("FNR", "narG", "-"),
        ("AraC", "araB", "+"),
        ("AraC", "araC", "+"),
        ("AraC", "araD", "+"),
    ]
    # Filtramos para quedarnos solo con CRP y AraC (FNR queda fuera)
    filtered_regulon = filter_by_min_genes(SAMPLE_REGULON, min_genes=2)
    filtered_interactions = filter_interactions_by_regulon(all_interactions, filtered_regulon)
    
    # Deben desaparecer las interacciones de FNR
    assert ("FNR", "narG", "-") not in filtered_interactions
    # Deben estar las de CRP y AraC
    assert ("CRP", "lacZ", "+") in filtered_interactions
    assert ("AraC", "araD", "+") in filtered_interactions
    assert len(filtered_interactions) == 5  # 2 de CRP + 3 de AraC