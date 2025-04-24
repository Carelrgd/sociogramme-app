import streamlit as st
from pyvis.network import Network
from streamlit.components.v1 import html
import tempfile
import os

st.set_page_config(page_title="Sociogramme Interactif", layout="centered")

st.title("Générateur de Sociogramme Interactif")

st.markdown("**Entrez les relations entre les personnes** (une par ligne, format : `Personne1,Personne2`)")

# Zone de texte pour saisir les relations
data_input = st.text_area("Relations", "Alice,Bob\nBob,Claire\nClaire,Alice\nDavid,Alice")

if st.button("Générer le sociogramme"):
    relations = []
    for line in data_input.strip().split("\n"):
        if "," in line:
            source, target = line.strip().split(",", 1)
            relations.append((source.strip(), target.strip()))

    # Création du graphe avec Pyvis
    net = Network(height="500px", width="100%", directed=True)
    net.barnes_hut()

    for source, target in relations:
        net.add_node(source, label=source)
        net.add_node(target, label=target)
        net.add_edge(source, target)

    # Sauvegarde temporaire du graphe
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        path = tmp_file.name
        net.save_graph(path)

        # Affichage dans Streamlit
        with open(path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            html(html_content, height=550, width=700)

    os.remove(path)
