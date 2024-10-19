#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import praw

def initialize_reddit():
    return praw.Reddit(
        client_id='lJdhPezmv9sqcGbvMmkBOQ',
        client_secret='1DKgLm1apKC35cVf2tByGy81-7AGUw',
        user_agent='desktop:com.example.dsci560:v1.0 (by /u/Pristine_Dealer7395)'

    )

