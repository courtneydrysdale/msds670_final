#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 17:31:34 2025

Title: MSDS 670 Final Project: Taylor Swift's Discography
Date: August 24, 2025
Author: Courtney Drysdale
Purpose: Explore Taylor Swift's discography over time

The dataset is from Kaggle:
    https://www.kaggle.com/datasets/jarredpriester/taylor-swift-spotify-dataset
'''
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dpi = 300

df = pd.read_csv("taylor_swift_spotify.csv", index_col=0)
columns = list(df.columns)

#Removing live albums and playlists
df = df[~df['album'].isin(['Live From Clear Channel Stripped 2008', 
                           'reputation Stadium Tour Surprise Song Playlist', 
                           'folklore: the long pond studio sessions (from the Disney+ special) [deluxe edition]', 
                           'Speak Now World Tour Live'])]

df.describe().T

#Checking for missing values
df.isnull().sum()

#Creating album_year field
df['album_year'] = df['release_date'].str[0:4] 
df['album_year'] = df['album_year'].astype(int)

#Checking to make sure all expected years were presentdf.album_year.unique() 
df_years = df[['album', 'album_year']]

year_counts = df['album_year'].value_counts()
counts_df = year_counts.reset_index()
counts_df.columns = ['Year', 'Count']

df_sorted = counts_df.sort_values(by='Year')

fig, ax = plt.subplots(figsize=(10,6))
line, = ax.plot(df_sorted["Year"], df_sorted["Count"])
ax.set_ylabel('Number of Songs')
ax.set_xticks(df_sorted["Year"])
ax.set_xticklabels(df_sorted["Year"])
ax.set_title('Number of Taylor Swift Songs Released by Year')

plt.tight_layout()

plot1_filename = 'songs_per_year.png'
fig.savefig(plot1_filename, dpi=dpi)

albums_year = df.groupby('album_year')['album'].nunique()

albums_df = albums_year.reset_index()
albums_df.columns = ['Year', 'Count']

from matplotlib.ticker import MaxNLocator

fig, ax = plt.subplots(figsize=(10,6))
line, = ax.plot(albums_df["Year"], albums_df["Count"])
ax.set_xticks(albums_df["Year"])
ax.set_xticklabels(albums_df["Year"])
ax.set_title('Number of Taylor Swift Albums Released by Year')
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

plot2_filename = 'albums_per_year.png'
fig.savefig(plot2_filename, dpi=dpi)

albums = df.groupby('album')['name'].count()
df_albums = albums.to_frame().reset_index()
df_albums_sorted = df_albums.sort_values('name', ascending=True)

fig, ax = plt.subplots(figsize=(10,8))
ax.barh(df_albums_sorted["album"], df_albums_sorted["name"])
ax.set_title('Number of Tracks by Album')

plt.tight_layout()

#Creating custom color map for albums
color_map = {                   
    "1989": 'lightblue',
    "1989 (Deluxe)": 'lightblue',
    "1989 (Taylor's Version)": 'lightblue',
    "1989 (Taylor's Version) [Deluxe]": 'lightblue',
    "Fearless (International Version)": 'gold',
    "Fearless (Platinum Edition)": 'gold',
    "Fearless (Taylor's Version)": 'gold',
    "Lover": 'lightpink',
    "Midnights": 'navy',
    "Midnights (3am Edition)": 'navy',
    "Midnights (The Til Dawn Edition)": 'navy',
    "Red": 'crimson',
    "Red (Deluxe Edition)": 'crimson',
    "Red (Taylor's Version)": 'crimson',
    "Speak Now": 'mediumpurple',
    "Speak Now (Deluxe Package)": 'mediumpurple',
    "Speak Now (Taylor's Version)": 'mediumpurple',
    "THE TORTURED POETS DEPARTMENT": 'dimgrey',
    "THE TORTURED POETS DEPARTMENT: THE ANTHOLOGY": 'dimgrey',
    "Taylor Swift (Deluxe Edition)": 'yellowgreen',
    "evermore": 'tan',
    "evermore (deluxe version)": 'tan',
    "folklore": 'silver',
    "folklore (deluxe version)": 'silver',
    "reputation": 'black'
}

colors = df_albums_sorted['album'].map(color_map)

fig, ax = plt.subplots(figsize=(8,6))
ax.barh(df_albums_sorted["album"], df_albums_sorted["name"], color=colors)
ax.set_title('Number of Tracks by Album')

plt.tight_layout()

plot3_filename = 'tracks_per_album.png'
fig.savefig(plot3_filename, dpi=dpi)

#Creating correlation matrix with seaborn
corr = df.corr()

fig, ax = plt.subplots(figsize=(10,8))
ax = sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)

plot4_filename = 'corr_matrix.png'
fig.savefig(plot4_filename, dpi=dpi)

fig, ax = plt.subplots(figsize=(10,6))
ax = sns.scatterplot(data=df, x='energy', y='loudness', hue='album', palette=color_map, legend=False)
plt.title('Energy vs. Loudness')

plt.tight_layout()

plot5_filename = 'evergy_loudness.png'
fig.savefig(plot5_filename, dpi=dpi)

fig, ax = plt.subplots(figsize=(10,6))
ax = sns.scatterplot(data=df, x='album_year', y='popularity', hue='album', palette=color_map, legend=False, alpha=0.5)
plt.title('Popularity vs. Album Year')
ax.set_xticks(albums_df["Year"])
ax.set_xticklabels(albums_df["Year"])
plt.tight_layout()

plot6_filename = 'popularity_album_year.png'
fig.savefig(plot6_filename, dpi=dpi)

popularity = df.groupby('album')['popularity'].mean()

df_pop = popularity.to_frame().reset_index()

df_pop = df_pop.sort_values('popularity', ascending=True)

colors_pop = df_pop['album'].map(color_map)

fig, ax = plt.subplots(figsize=(8,6))
ax.barh(df_pop["album"], df_pop["popularity"], color=colors_pop)
ax.set_title('Mean Popularity by Album')

plt.tight_layout()

plot7_filename = 'popularity_by_album.png'
fig.savefig(plot7_filename, dpi=dpi)

pop_sorted = df.sort_values('popularity', ascending=False)

df_top20 = pop_sorted.head(20)

colors_pop = df_top20['album'].map(color_map)

fig, ax = plt.subplots(figsize=(8,6))
ax.barh(df_top20["name"], df_top20["popularity"], color=colors_pop)
ax.invert_yaxis()
ax.set_title('Top 20 Most Popular Songs')

plt.tight_layout()

plot8_filename = 'top20_songs.png'
fig.savefig(plot8_filename, dpi=dpi)