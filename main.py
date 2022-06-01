
import streamlit as st

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from karateclub.dataset import GraphSetReader
from karateclub import FeatherGraph
from sklearn.model_selection import train_test_split
import networkx as nx

import itertools

from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression

import praw
from praw.models import MoreComments

import logging

from utils.utils import *

# ---

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
    number_posts_to_load = st.number_input('Number of posts to load', int(2), key=key)

    if first_run_str not in st.session_state:
        st.session_state[first_run_str] = True
    if graph_str not in st.session_state:
        st.session_state[graph_str] = []

    if st.button('Load graphs', key=key):
        st.session_state[first_run_str] = False
        st.session_state[graph_str] = get_graphs_from_subreddit_name(subreddit_name, number_posts_to_load)

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


st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

with col1:
    col_content(1)

with col2:
    col_content(2)
