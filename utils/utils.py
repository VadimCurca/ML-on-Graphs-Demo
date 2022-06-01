import praw
import itertools
import networkx as nx
import re

from praw.models import MoreComments

def get_graphs_indices_from_subreddit(subreddit, limit=1):
    list_graphs = []
    list_titles = []
    for submission in subreddit.hot(limit=limit):
        print(submission.title)

        G = nx.Graph()
        nodes, edges = get_graph_indices_from_submission(submission, limit=100)

        if(G.edges == []):
            continue

        G.add_edges_from(edges)
        G.add_nodes_from(nodes)

        print(G.number_of_nodes())

        list_graphs.append(G)
        list_titles.append(submission.title)
    return list_graphs, list_titles

def get_graphs_from_file(file_name):
    graphs = []
    titles = []

    with open(file_name, 'r') as f:
        number_of_graphs_str = f.readline()
        number_of_graphs = int(re.findall('\d+', number_of_graphs_str)[0])

        for graphs_idx in range(number_of_graphs):
            title = f.readline().strip()

            G = nx.Graph()

            line = f.readline()
            number_of_nodes = int(re.findall('\d+', line)[0])
            line = f.readline()
            number_of_edges = int(re.findall('\d+', line)[0])

            G.add_nodes_from(list(range(number_of_nodes)))

            for edges_idx in range(number_of_edges):
                line = f.readline()
                edge_lst = re.findall('\d+', line)

                G.add_edge(int(edge_lst[0]), int(edge_lst[1]))

            graphs.append(G)
            titles.append(title)
    return graphs, titles

def get_authors_from_comments(comment_list):
    return list(comment.author for comment in comment_list if comment.author != None)


def get_graph_names_from_submission(submission, limit=None):
    submission.comments.replace_more(limit=limit)

    graph_list = []
    comment_queue = submission.comments[:]

    authors = get_authors_from_comments(comment_queue)
    graph_list = list(zip(itertools.repeat(submission.author), authors))

    while comment_queue:
        comment = comment_queue.pop(0)
        if(comment.author != None):
            authors = get_authors_from_comments(comment.replies)
            graph_list += list(zip(itertools.repeat(comment.author), authors))

        comment_queue.extend(comment.replies)

    authors = get_authors_from_comments(submission.comments.list())

    return (authors, graph_list)


def comments_to_ids(comments, name_to_id):
    l = []
    for comment in comments:
        if comment.author == None:
            continue
        id = name_to_id.get(comment.author)
        if id == None:
            lg = len(name_to_id)
            name_to_id[comment.author] = lg;
            id = lg
        l.append(id)
    return l


def get_graph_indices_from_submission(submission, limit=None):
    submission.comments.replace_more(limit=limit)

    graph_list = []
    comment_queue = submission.comments[:]

    name_to_id = {}
    name_to_id[submission.author] = 0

    l = comments_to_ids(comment_queue, name_to_id)
    graph_list = list(zip(itertools.repeat(0), l))

    while comment_queue:
        comment = comment_queue.pop(0)

        comment_replies = list(comment.replies)
        comment_queue.extend(comment_replies)

        if comment.author != None:
            l = comments_to_ids(comment_replies, name_to_id)
            this_id = comments_to_ids([comment], name_to_id)[0]
            graph_list += list(zip(itertools.repeat(this_id), l))


    return list(range(len(name_to_id))), graph_list
