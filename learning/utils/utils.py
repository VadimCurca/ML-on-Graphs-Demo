import itertools

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
