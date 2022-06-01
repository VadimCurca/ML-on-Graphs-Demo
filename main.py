
import streamlit as st

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

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
    graphs = get_graphs_indices_from_subreddit(subreddit, number_posts_to_load)
    return graphs

subreddit_name = st.text_input('Subreddit name', 'hardware')
number_posts_to_load = st.number_input('Number of posts to load', int(2))

if 'first_run' not in st.session_state:
    st.session_state['first_run'] = True
if 'graph' not in st.session_state:
    st.session_state['graph'] = []

if st.button('Load graphs'):
    st.session_state['first_run'] = False
    st.session_state['graph'] = get_graphs_from_subreddit_name(subreddit_name, number_posts_to_load)

if st.session_state['first_run'] == False:
    post_number = st.number_input('Which post to show', 0)

    G = st.session_state['graph']

    fig = plt.figure(figsize = (15, 15))
    nx.draw_kamada_kawai(G[post_number], with_labels=True, width = .5)
    st.pyplot(fig)
