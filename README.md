# IC_project


The scope of this project is to see if we can classify the posts of 2 different communities (subrredits) based solely on how people comment and interact with each other.  
  
In the demo, I extract data from reddit and make a graph from the comments section of each post, where each comment author is a node and replies between them are edges. Then I compute graph embeddings to get features for each graph and classify them with a logistic regression.  
  
Taking the "food" and "hardware" communities, I uploaded approximately 850 posts from each subreddit (/subreddit/hot thread), dividing the dataset into 80% train and 20% test, I got an ~86% accuracy on the test dataset.  
After the model is trained we can take any post from the 2 communities used, paste the link into the coresponding text box and make a prediction for it. For representative posts (number of nodes > 10) the model gives very good results, with predicted probabilities > 90%.  
  
I use `praw` to extract data, `networkx` to create graphs, `karate club` to compute graph embeddings, `sklearn` for logistic regression and `streamlit` for frontend.  
  
![ezgif com-gif-maker (4)](https://user-images.githubusercontent.com/80581374/171453955-66e36358-5da6-4169-b578-a853e8216fa3.gif)

<br>

Credits to: [Zademn](https://github.com/zademn/netsci-labs)  
  
[Project slides](https://docs.google.com/presentation/d/1twZQt5kfJM_3CR6FvFMjb7uANKvTazUnuf5gkDw7zJ4/edit?usp=sharing)
