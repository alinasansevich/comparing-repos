#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 15:41:11 2020

@author: alina

from "Python Crash Course", chapter 17,
"Working with APIs", exercise 17-1:

17-1. Other Languages: Modify the API call in python_repos.py so it generates
a chart showing the most popular projects in other languages. Try languages
such as JavaScript, Ruby, C, Java, Perl, Haskell, and Go.

exploring what info I can get from this API call
"""

import requests

language = 'python'

url = 'https://api.github.com/search/repositories?q=language:{}&sort=stars'
url = url.format(language)
r = requests.get(url)
print("{} status code:".format(language.capitalize()), r.status_code)

# Store API response in a variable.
response_dict = r.json()
print("{} total repositories:".format(language.capitalize()), 
      response_dict['total_count'])
    
# Explore information about the repositories.
repo_dicts = response_dict['items']
print("Repositories returned:", len(repo_dicts))

# Examine the first repository.
repo_dict = repo_dicts[0]
print("\nKeys:", len(repo_dict))
for key in sorted(repo_dict.keys()):
    print(key)

contributors_urls = {}
print("\nSelected information about each repository:")
for repo_dict in repo_dicts:
    # print('Name:', repo_dict['name'])
    # print('Owner:', repo_dict['owner']['login'])
    # print('Stars:', repo_dict['stargazers_count'])
    # print('Repository:', repo_dict['html_url'])
    # print('Created:', repo_dict['created_at'])
    # print('Updated:', repo_dict['updated_at'])
    # print('Description:', repo_dict['description'], '\n\n')
    # print('Contributors:', repo_dict['contributors_url'])
    contributors_urls[repo_dict['name']] = repo_dict['contributors_url']
    
def get_contributors_num(contributors_dict):
    """
    (dict) -> dict

    Returns a new dict, with the repos names as keys
    and the number of contributors as values.
    """
    num_contributors = {}
    
    for k, v in contributors_dict.items():
        url = v + '?page=1&per_page=1000'
        r = requests.get(url)
        
        response_dict = r.json()
        num_contributors[k] = len(response_dict)
    
    return num_contributors

num_contributors = get_contributors_num(contributors_urls)
# ?page=1&per_page=1000

# Plot.
names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    plot_dict = {
        'value': repo_dict['stargazers_count'],
        'label': repo_dict['description'] or '', # this line raised an error
        'xlink': repo_dict['html_url'],
        }
    plot_dicts.append(plot_dict)