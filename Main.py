import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Reading the Fandango's Data

fandango=pd.read_csv("fandango_scrape.csv")

#Checking the heads of the DataFrame ( optional )
# print(fandango.head())

#Let's explore the relationship between popularity of a film and its rating by creating a  scatterplot showing the relationship between rating and votes

plt.figure()  # Create a new figure
sns.scatterplot(data=fandango, x="RATING", y="VOTES", alpha=1)
plt.title("Rating vs Votes")

#Creating a new column that is able to strip the year from the title strings and set this new column as YEAR
fandango['YEAR']=fandango['FILM'].apply(lambda title:title.split('(') [-1].replace(')'," "))
#print(fandango.head())        Just to verify the changes made

#Visualizing the Count of movie per year with a plot
plt.figure()  # Create another new figure
sns.countplot(data=fandango, x='YEAR',palette="magma")
plt.title("Movie Count per Year")

#Creating DataFrame of only reviewed films by removing any films that have zero votes
fan_reviewed=fandango[fandango['VOTES']>0]

#Create a KDE plot  that displays the distribution of ratings that are displayed (STARS) v/s what the true rating was from votes (RATING). Clip the KDEs to 0-5.
plt.figure()
sns.kdeplot(data=fan_reviewed,x="RATING",clip=[0,5],fill=True,label="True Ratings")
sns.kdeplot(data=fan_reviewed,x="STARS",clip=[0,5],fill=True,label="Stars Displayed")
plt.legend()
plt.title("Stars v/s Rating")

#Let's now actually quantify this discrepancy. Create a new column of the different between STARS displayed versus true RATING.
fan_reviewed["STARS_DIFF"]=fan_reviewed['STARS']-fan_reviewed["RATING"]
fan_reviewed["STARS_DIFF"]=fan_reviewed["STARS_DIFF"].round(2 )

#Create a count plot to display the number of times a certain difference occurs
plt.figure()
sns.countplot(data=fan_reviewed,x="STARS_DIFF",palette="magma")
plt.title("Difference count")

#Now Reading another Dataset which contain data of the rating of different movies on different rating websites

all_sites=pd.read_csv("all_sites_scores.csv")


#Create a scatterplot exploring the relationship between RT Critic reviews and RT User reviews
plt.figure()
sns.scatterplot(data=all_sites,x="RottenTomatoes",y="RottenTomatoes_User")
plt.xlim(0,100)
plt.ylim(0,100)

#Create a new column based off the difference between critics ratings and users ratings for Rotten Tomatoes. Calculate this with RottenTomatoes-RottenTomatoes_User
all_sites['Rotten_Diff']  = all_sites['RottenTomatoes'] - all_sites['RottenTomatoes_User']


#Plot the distribution of the differences between RT Critics Score and RT User Score
plt.figure()
sns.histplot(data=all_sites,x='Rotten_Diff',kde=True,bins=25)
plt.title("RT Critics Score minus RT User Score")


#Display a scatterplot of the Metacritic Rating versus the Metacritic User rating
plt.figure()
sns.scatterplot(data=all_sites,x='Metacritic',y='Metacritic_User')
plt.xlim(0,100)
plt.ylim(0,10)

#Create a scatterplot for the relationship between vote counts on MetaCritic versus vote counts on IMDB
plt.figure()
sns.scatterplot(data=all_sites,x='Metacritic_user_vote_count',y='IMDB_user_vote_count')

'''Combine the Fandango Table with the All Sites table.
Not every movie in the Fandango table is in the All Sites table, since some Fandango movies have very little or no reviews.
We only want to compare movies that are in both DataFrames, so do an *inner* merge to merge together both DataFrames based on the FILM columns'''

df = pd.merge(fandango,all_sites,on='FILM',how='inner')

#Create new normalized columns for all ratings so they match up within the 0-5 star range shown on Fandango
#Dont run this cell multiple times, otherwise you keep dividing!
df['RT_Norm'] = np.round(df['RottenTomatoes']/20,1)
df['RTU_Norm'] =  np.round(df['RottenTomatoes_User']/20,1)
df['Meta_Norm'] =  np.round(df['Metacritic']/20,1)
df['Meta_U_Norm'] =  np.round(df['Metacritic_User']/2,1)
df['IMDB_Norm'] = np.round(df['IMDB']/2,1)

#Now create a norm_scores DataFrame that only contains the normalizes ratings. Include both STARS and RATING from the original Fandango table
norm_scores = df[['STARS','RATING','RT_Norm','RTU_Norm','Meta_Norm','Meta_U_Norm','IMDB_Norm']]

#Create a plot comparing the distributions of normalized ratings across all sites. There are many ways to do this, but explore the Seaborn KDEplot docs for some simple ways to quickly show this. Don't worry if your plot format does not look exactly the same as ours, as long as the differences in distribution are clear
def move_legend(ax, new_loc, **kws):
    old_legend = ax.legend_
    if old_legend:
        handles = old_legend.legend_handles
        labels = [t.get_text() for t in old_legend.get_texts()]
        title = old_legend.get_title().get_text()
        ax.legend(handles, labels, loc=new_loc, title=title, **kws)


fig, ax = plt.subplots(figsize=(15,6),dpi=150)
sns.kdeplot(data=norm_scores,clip=[0,5],shade=True,palette='Set1',ax=ax)
move_legend(ax, "upper left")

#Clearly Fandango has an uneven distribution. We can also see that RT critics have the most uniform distribution. Let's directly compare these two.
fig, ax = plt.subplots(figsize=(15,6),dpi=150)
sns.kdeplot(data=norm_scores[['RT_Norm','STARS']],clip=[0,5],shade=True,palette='Set1',ax=ax)
move_legend(ax, "upper left")

#Create a histplot comparing all normalized scores
plt.subplots(figsize=(15,6),dpi=150)
sns.histplot(norm_scores,bins=50)
plt.show()