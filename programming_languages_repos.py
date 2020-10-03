#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:09:12 2020

@author: alina

from "Python Crash Course", chapter 17,
"Working with APIs", exercise 17-1:

17-1. Other Languages: Modify the API call in python_repos.py so it generates
a chart showing the most popular projects in other languages. Try languages
such as JavaScript, Ruby, C, Java, Perl, Haskell, and Go.
"""

import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

languages = ['python',
             'javascript',
             'ruby',
             'c',
             'java',
             'perl',
             'haskell',
             'go']

colors = ['#333366',
          '#ff0000',
          '#e0115f',
          '#a9a9a9',
          '#e08b3e',
          '#90ee90',
          '#ffff00',
          '#e53fe5']

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

# Make an API call and store the response.

for language in languages:
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
    
    # Make visualization.
    my_style = LS('{}'.format(colors[languages.index(language)]), base_style=LCS)
    
    chart = pygal.Bar(my_config, style=my_style)
    # chart = pygal.Bar(style=my_style, x_label_rotation=45, show_legend=False)
    chart.title = 'Most-Starred {} Projects on GitHub'.format(language.capitalize())
    chart.x_labels = names
    
    # chart.add('', stars)
    chart.add('', plot_dicts)
    chart.render_to_file('{}_repos.svg'.format(language))

