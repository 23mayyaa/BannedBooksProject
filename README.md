# Banned Books Project
## MadData 2025 Submission
### Chieler Li, Steve Lin, Aniruddh Mayya, Sanjay Murali

## Libraries
Can be found in requirements.txt
- pandas
- streamlit
- folium
- scikit-learn

## Inspiration
We were inspired by the mission of PEN America in fighting book bans in the US.

## Functionality
The program takes user input for title and author and uses a model to predict the likelihood of a book being banned, based on title, description, and genre. The model is trained on data scraped from GoodReads.

## Methodology
We scraped data on GoodReads about banned and non-banned books, and trained a sci-kit Learn  XGBoost classifier to classify book as likely to be banned based on the aforementioned features.
The user inputs a title and author and we scrape GoodReads to get it's information, then use our model to classify it.

## Challenges
We found that scraping took a large portion of our time, as the number of books we chose was very large. Of course, the 24 hour time constraint was also a challenge.

## Accomplishments
We were able to create a large dataset through scraping GoodReads.

## Learnings
We learnt a lot about web scraping, as well as using Streamlit for making a frontend directly in our python file. 

## What's Next
Our team wants to flesh out the program more, perhaps find more feautures to improve the model.
