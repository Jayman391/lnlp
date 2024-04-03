from bertopic import BERTopic
import os
import pandas as pd
from util._session import Session
from drivers._global_driver import GlobalDriver
from util._formatter import DataFormatter
from viz._tm_viz import visualize, _visualize_topics, _visualize_documents, _visualize_terms,_visualize_word_shifts, _visualize_heatmap_from_df, _visualize_power_danger_structure, _process_dataframe_for_visualization, _safe_read_csv

session = Session()

model = BERTopic()

data = _safe_read_csv(file_path="tests/test_data/brazil-vaccine-comments.csv", session=session)

docs = data["text"].tolist()[:1000]

session.set_data(docs)

topics, _ = model.fit_transform(docs)

os.makedirs("output", exist_ok=True)


""" def test_visualize_topics():
    _visualize_topics(model, session, 'output')
    assert os.path.exists("output/topic_viz.html")
    assert os.path.exists("output/hierarchical_viz.html")
    assert os.path.exists("output/heatmap.html")

def test_visualize_documents():
    _visualize_documents(model, session, 'output')
    assert os.path.exists("output/document_viz.html")
    assert os.path.exists("output/hierarchical_document_viz.html")

def test_visualize_terms():
    _visualize_terms(model, session, 'output')
    assert os.path.exists("output/term_viz.html")
"""
def test_visualize_word_shifts():
    pass

def test_process_dataframe_for_visualization():
    pass

def test_visualize_heatmap_from_df():
    pass

def test_visualize_power_danger_structure():
    pass

def test_visualize():
    pass 
