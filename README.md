# **Wisdom of the Tribe**
### A data science project 

---

What film should you go see this weekend? To answer this question, one can check the film ratings on rottentomatoes.com or metacritic.com to get an idea of the **wisdom of the masses**. The purpose of this project is to provide a **wisdom of the tribe** alternative for movie recommendations. This is accomplished by developing a collaborative recommendation system. Specifically, by defining a subset of movie critics with film preferences similar to an individual user and providing film recommendations (rating predictions) based on each users 'tribe' of film critics. 

### User Value: 

* Updated Film Rating Predictions (tribe-based)
* Rank Listing of Tribe Members (film critics with highest preference match)

### Marketing Value:

* With enough users, clustering can illuminate genre-bending film niches.
* May allow for more successful user-based advertisements and product recommendations.

---

### Approach: 

**Data Gathering**
- [x] Obtain a list of the top 500 grossing (in the US) films for every year from 1980 until today (190,000 films) from [IMDB.com](http://www.IMDB.com) via webscraping. 
- [x] Obtain film information (e.g., release date, genres) and reviewer ratings for each available film on [metacritic.com](http://www.metacritic.com) via webscraping. 
- [x] Design SQL database for storing film and review data.
![db](https://raw.githubusercontent.com/jmolds/widsom-of-the-tribe/master/data-images-etc/database%20design.png)

**Data Transformation**
- [X] Generate by-film-scaled ratings to empahsize deviations from the crowd. 
- [X] Generate by-reviewer-scaled ratings to emphasize deviations from an individual reviewer's baseline. 
- [X] Update by-film-scaled ratings using any available by-reviewer scaled values.

**Model Development**
- [X] Straightforward user-reviewer similary model.
- [ ] Neural Network based model using Tensorflow.

**Model Evaluation**
- [ ] Compare cross-validation prediciton error of user-reviewer models with ratings from [rottentomatoes.com](http://www.rottentomatoes.com) and [metacritic.com](http://www.metacritic.com).

**Visualization**

- [ ] Develop a 3d scatterplot (using Plotly) of reviewers by similarity, confidence, and clustered by genre. 