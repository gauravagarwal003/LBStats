from functions import *
import csv
from datetime import datetime
import time
requestsSession = requests.Session()

def store_data(id, label, number, filename='stats.csv'):
    # Get the current date in YYYY-MM-DD format
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Open the CSV file in append mode ('a')
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # If this is the first time you're writing to the file, include the header
        csvfile.seek(0, 2)  # Move to the end of the file
        if csvfile.tell() == 0:  # If file is empty, write the header
            writer.writerow(['id', 'label', 'date', 'number'])
        
        # Write the new data (ID, Label, Date, Number)
        writer.writerow([id, label, current_date, number])

time_total = time.time()
base_url = "https://letterboxd.com/sprudelheinz/list/all-the-movies-sorted-by-movie-posters-1/by/popular/"
page_number = 1
while page_number <= 5:
    url = f"{base_url}/page/{page_number}/"
    response = requestsSession.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    movie_divs = soup.find_all('div', class_='really-lazy-load')
    if not movie_divs:
        break
    for div in movie_divs:
        time_each_movie = time.time()
        movieID = div['data-film-slug']
        responseLikes = requestsSession.get(f"https://letterboxd.com/film/{movieID}/likes")
        soupLikes = BeautifulSoup(responseLikes.text, 'lxml')
        
        responseRating = requestsSession.get(f"https://letterboxd.com/csi/film/{movieID}/rating-histogram/")
        soupRating = BeautifulSoup(responseRating.text, 'lxml')

        store_data(movieID, "numViews", getnumViews(True, movieID, soupLikes))
        store_data(movieID, "avgRating", getAverageRating(True, movieID, soupRating))
        store_data(movieID, "numReviews", getNumReviews(True, movieID))
        store_data(movieID, "numRatings", getNumRatings(True, movieID))
        store_data(movieID, "numLikes", getNumLikes(True,movieID, soupLikes))
        store_data(movieID, "numFans", getNumFans(True, movieID, soupLikes))
        print(f"{movieID} took {time.time() - time_each_movie} seconds")
    page_number += 1
print(f"Total time: {time.time() - time_total}. Finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")