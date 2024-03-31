import pandas as pd
import os
import math
import webbrowser
from webbrowser import open_new_tab
from bertopic import BERTopic
from src.util._session import Session
from src.viz._ous_viz import HeatMaps
import sys
import shifterator as sh
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

if sys.platform.startswith("linux"):
    file = ""
else:
    file = "file://"

def visualize(model: BERTopic, session:Session , directory: str = "", data: list = []):
        plotting = [log for log in data if "Plotting" in log.keys()]
        session.logs["info"].append("Plotting Topics")
        if len(plotting) > 0:
            for log in plotting:
                value = str(list(log.values())[0])
                if (
                    str(value) == "firefox"
                    or value == "chrome"
                    or value == "safari"
                    or value == "opera"
                ):
                    webbrowser.register(value, None, webbrowser.BackgroundBrowser)
                if (
                    str(value) != "firefox"
                    and value != "chrome"
                    and value != "safari"
                    and value != "opera"
                    and not "Enable" in value
                ):
                    directory = value
            for log in plotting:
                value = str(list(log.values())[0])
                if "Enable Topic Visualizations" in value:
                    print("Visualizing Topics")
                    _visualize_topics(model, session, directory)
                    session.logs["info"].append("Visualizing Topics")
                if "Enable Document Visualizations" in value:
                    print("Visualizing Documents")
                    _visualize_documents(model, session, directory)
                    session.logs["info"].append("Visualizing Documents")
                if "Enable Term Visualizations" in value:
                    print("Visualizing Terms")
                    _visualize_terms(model, session, directory)
                    session.logs["info"].append("Visualizing Terms")
                if "Enable All Visualizations" in value:
                    print("Visualizing All")
                    _visualize_topics(model, session, directory)
                    _visualize_documents(model, session, directory)
                    _visualize_terms(model, session, directory)
                    session.logs["info"].append("Visualizing All")
                if "Enable Word Shift Graphs" in value:
                    _visualize_word_shifts(session, directory)
                    session.logs["info"].append("Visualizing Word Shifts")
                if "Enable Power Danger Structure Graphs" in value:
                    _visualize_power_danger_structure(session, directory)
                    session.logs["info"].append("Visualizing Power Danger Structure Graphs")
        else:
            print(
                "No plotting options selected. Visualizing all topics, documents, and terms by default."
            )
            #_visualize_topics(model, session, directory)
            #_visualize_terms(model, session, directory)
            #_visualize_word_shifts(session, directory)
            _visualize_power_danger_structure(session, directory)                                                            
            _visualize_documents(model, session, directory)

            session.logs["info"].append("Visualizing All")

def _visualize_topics(model: BERTopic, session:Session , directory: str = ""):
    try:
        topic_viz = model.visualize_topics()
        if directory != "":
            topic_viz.write_html(f"{directory}/topic_viz.html")
            webbrowser.open_new(
                file + os.path.realpath(f"{directory}/topic_viz.html")
            )
        else:
            topic_viz.write_html("topic_viz.html")
            webbrowser.open_new(file + os.path.realpath(f"topic_viz.html"))

    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e))

    try:
        hierarchical_topics = model.hierarchical_topics(docs=session.data)
        hierarchical_viz = model.visualize_hierarchy(
            hierarchical_topics=hierarchical_topics
        )

        if directory != "":
            hierarchical_viz.write_html(f"{directory}/hierarchical_viz.html")
            webbrowser.open_new(
                file + os.path.realpath(f"{directory}/hierarchical_viz.html")
            )
        else:
            hierarchical_viz.write_html("hierarchical_viz.html")
            webbrowser.open_new(file + os.path.realpath("hierarchical_viz.html"))
    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e))

    try:
        heatmap = model.visualize_heatmap()

        if directory != "":
            heatmap.write_html(f"{directory}/heatmap.html")
            webbrowser.open_new(
                file + os.path.realpath(f"{directory}/heatmap.html")
            )
        else:
            heatmap.write_html("heatmap.html")
            webbrowser.open_new(file + os.path.realpath(f"heatmap.html"))
    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e))

def _visualize_documents( model: BERTopic, session:Session , directory: str = ""):
    try:
        doc_viz = model.visualize_documents(docs=session.data, sample=0.05)

        if directory:
            doc_viz.write_html(f"{directory}/document_viz.html")
            webbrowser.open_new(
                file + os.path.realpath(f"{directory}/document_viz.html")
            )
        else:
            doc_viz.write_html("document_viz.html")
            webbrowser.open_new(file + os.path.realpath("document_viz.html"))
    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e))

    try:
        hierarchical_topics = model.hierarchical_topics(docs=session.data)
        hierarchical_docs = model.visualize_hierarchical_documents(
            docs=session.data,
            hierarchical_topics=hierarchical_topics,
            embeddings=model._extract_embeddings(session.data),
            nr_levels=math.ceil(math.sqrt(len(hierarchical_topics) // 2)),
            level_scale="log",
        )

        if directory:
            hierarchical_docs.write_html(
                f"{directory}/hierarchical_document_viz.html"
            )
            webbrowser.open_new(
                file
                + os.path.realpath(f"{directory}/hierarchical_document_viz.html")
            )
        else:
            hierarchical_docs.write_html("hierarchical_document_viz.html")
            webbrowser.open_new(
                file + os.path.realpath("hierarchical_document_viz.html")
            )
    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e))

def _visualize_terms( model: BERTopic, session:Session , directory: str = ""):
    try:
        terms = model.visualize_barchart(top_n_topics=500, n_words=10)

        if directory:
            terms.write_html(f"{directory}/term_viz.html")
            webbrowser.open_new(
                file + os.path.realpath(f"{directory}/term_viz.html")
            )
        else:
            terms.write_html("term_viz.html")
            webbrowser.open_new(file + os.path.realpath("term_viz.html"))
    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e))
    
def _visualize_word_shifts(session:Session, directory: str = ""):
    try:
        # in directory, there is a sub directory named topics. For each topic, there is a file named topic_zipf.csv
        # and topic_sample_zipf.csv.
        # get all files in directory/topics 
        files = os.listdir(f"{directory}/topics")
        samples = [f for f in files if "sample" in f]
        files = [f for f in files if "sample" not in f]
        if len(samples) != len(files):
            raise ValueError("Number of topics must equal number of samples")
        
        labmt = pd.read_csv('src/viz/LABMT.csv')

        # calculate sentiment of corpus

        lens_min = 4
        lens_max = 6

        for i, file in enumerate(files):

            topic_words = pd.read_csv(f"{directory}/topics/{file}")
            sample_words = pd.read_csv(f"{directory}/topics/{samples[i]}")
    
            # turn the types and counts columns into dicts
            topic_words = dict(zip(topic_words['types'], topic_words['counts']))

            sample_words = dict(zip(sample_words['types'], sample_words['counts']))

            # filter through lens
            topic_words = {k:v for k,v in topic_words.items() if k in labmt['Word'].values and (labmt[labmt['Word'] == k]['Happiness Score'].values[0] < lens_min or labmt[labmt['Word'] == k]['Happiness Score'].values[0] > lens_max)}

            sample_words = {k:v for k,v in sample_words.items() if k in labmt['Word'].values and (labmt[labmt['Word'] == k]['Happiness Score'].values[0] < lens_min or labmt[labmt['Word'] == k]['Happiness Score'].values[0] > lens_max)}

            sample_total_counts = sum(sample_words.values())
            
            if sample_total_counts:

                sample_sentiment = {k:v/sample_total_counts * labmt[labmt['Word'] == k]['Happiness Score'].values[0] for k,v in sample_words.items()}
                sample_full_sentiment = sum(sample_sentiment.values())

                shift_graph = sh.WeightedAvgShift(type2freq_1=sample_words, type2freq_2=topic_words, type2score_1="labMT_English",
                                                type2score_2="labMT_English", reference_value=sample_full_sentiment, handle_missing_scores="exclude")
            
                plt.figure(figsize=(10, 10))

                g = shift_graph.get_shift_graph()
            
                plt.savefig(f"{directory}/topics/{file.split(sep='.')[0]}_wordshift.png")

                plt.close()

    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e))

def _visualize_power_danger_structure(session:Session, directory: str = ""):
    try:

        ous = pd.read_csv('src/viz/NRC-VAD.txt', delimiter = ' ')

        files = os.listdir(f"{directory}/topics")
        files = [f for f in files if "sample" not in f]

        for _, file in enumerate(files):
            df = pd.read_csv(f"{directory}/topics/{file}")
            df = df[df['types'].isin(ous['word'])]

            df = df.merge(ous, left_on='types', right_on='word')
            #df.set_index('types', inplace=True)
            df.drop(columns=['counts', 'word','types'], inplace=True)

            svd = TruncatedSVD(n_components=3)
            svd.fit(df)
            df = svd.transform(df)
            df = pd.DataFrame(df, columns=['x', 'y', 'z'])
            df.index = df.index.astype(str)

            # get the 2 largest components X AND Y and rotate them by 90 degrees
            df['x'] = df['x'] * math.pi / 4
            df['y'] = df['y'] * math.pi / 4

            df.rename(columns={'x': 'Power', 'y': 'Danger', 'z': 'Structure'}, inplace=True)

            plt.figure(figsize=(10, 10))
            pow_dan = HeatMaps.generate_heatmap_from_df(df, 'Power', 'Danger')
            plt.savefig(f"{directory}/topics/{file.split(sep='.')[0]}_power_danger.png")
            plt.close()

            plt.figure(figsize=(10, 10))
            pow_str = HeatMaps.generate_heatmap_from_df(df, 'Power', 'Structure')
            plt.savefig(f"{directory}/topics/{file.split(sep='.')[0]}_power_structure.png")
            plt.close()

            plt.figure(figsize=(10, 10))
            dan_str = HeatMaps.generate_heatmap_from_df(df, 'Danger', 'Structure')
            plt.savefig(f"{directory}/topics/{file.split(sep='.')[0]}_danger_structure.png")
            plt.close()
            
       
    except Exception as e:
        print(e)
        session.logs["errors"].append(str(e))
