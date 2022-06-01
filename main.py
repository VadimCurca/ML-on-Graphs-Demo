
import streamlit as st

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from karateclub.dataset import GraphSetReader
from karateclub import FeatherGraph
from sklearn.model_selection import train_test_split
import networkx as nx
from karateclub import FeatherGraph
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import itertools
import copy

from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression

import praw
from praw.models import MoreComments

import logging

from utils.utils import *

# ---

cached_subreddits = {"hardware" : "graphsHardware.txt", "food" : "graphsFood.txt"}

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_graphs_from_subreddit_name(subreddit_name, number_posts_to_load):
    client_id = '8Ara-tL3whPJTKSzuLe0Wg'
    client_secret = '5ciIZ_875ywNSWHWY7S4QcaimF788g'
    user_agent = '<console:IC_proiect:1.0>'

    reddit = praw.Reddit(client_id = client_id,
                        client_secret = client_secret,
                        user_agent = user_agent)

    st.write("Cache miss: expensive_computation ")

    subreddit = reddit.subreddit(subreddit_name)
    return get_graphs_indices_from_subreddit(subreddit, number_posts_to_load)


def col_content(key):
    first_run_str = 'first_run' + str(key)
    graph_str = 'graph' + str(key)

    default_subreddit_name = ""
    if(key == 1):
        default_subreddit_name = "hardware"
    else:
        default_subreddit_name = "food"

    subreddit_name = st.text_input('Subreddit name', default_subreddit_name, key=key)
    cached_graphs = False
    if subreddit_name in cached_subreddits:
        cached_graphs = st.checkbox('Use cached graphs', value=True, key=key)

    if not cached_graphs:
        number_posts_to_load = st.number_input('Number of posts to load', int(5), key=key)

    if st.button('Load graphs', key=key):
        st.session_state[first_run_str] = False

        if(not cached_graphs):
            st.session_state[graph_str] = get_graphs_from_subreddit_name(subreddit_name, number_posts_to_load)
        else:
            file_name = cached_subreddits[subreddit_name]
            st.session_state[graph_str] = get_graphs_from_file(file_name)

    if st.session_state[first_run_str] == False:
        graphs, titles = st.session_state[graph_str]

        post_number = st.number_input('Which post to show', value=1, min_value=1, max_value=len(graphs), key=key)
        post_number -= 1

        G = graphs[post_number]

        fig = plt.figure(figsize = (15, 15))
        plt.title(titles[post_number])
        nx.draw_kamada_kawai(G, with_labels=True, width = .5)
        st.pyplot(fig)

        index = []
        tableData = []

        # To Do: add more attributes
        index += ["Number of nodes"]
        tableData += [G.number_of_nodes()]
        index += ["Number of edges"]
        tableData += [G.number_of_edges()]
        index += ["density"]
        tableData += [nx.density(G)]

        df = pd.DataFrame(tableData, index=index)
        st.table(df)


def compute_graphs_embedding_and_train():
    graph1_orig, _ = st.session_state["graph1"]
    graph2_orig, _ = st.session_state["graph2"]

    graph1 = copy.deepcopy(graph1_orig)
    graph2 = copy.deepcopy(graph2_orig.copy())

    graphs = graph1 + graph2
    targets = [0]*len(graph1) + [1]*len(graph2)

    model = FeatherGraph()
    model.fit(graphs)
    X = model.get_embedding()

    X_train, X_test, y_train, y_test = train_test_split(X, targets, test_size=0.2)

    downstream_model = LogisticRegression(max_iter=500).fit(X_train, y_train)

    st.session_state["model"] = model
    st.session_state["downstream_model"] = downstream_model
    st.session_state["downstream_model_score"] = downstream_model.score(X_test, y_test)


graph_str_list = ["graph1", "graph2"]

if "first_run1" not in st.session_state:
    st.session_state["first_run1" ] = True
if "first_run2" not in st.session_state:
    st.session_state["first_run2" ] = True

for graph_str in graph_str_list:
    if graph_str not in st.session_state:
        st.session_state[graph_str] = []


st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

with col1:
    col_content(1)

with col2:
    col_content(2)

if st.session_state["first_run1"] == False and st.session_state["first_run2"] == False:
    st.markdown("---")
    st.markdown("## Graphs classification")


    if st.button("Compute graphs embedding and train"):
        compute_graphs_embedding_and_train()
    
    if "downstream_model" in st.session_state:
        score = st.session_state["downstream_model_score"]
        st.write("test score: ", score)





        