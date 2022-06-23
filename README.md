# **Web-Scraper**

## **Milestone 1: Choosing a website**
---

Choosing a website to scrape was a hard choice. While it is easy to choose Google, Facebook, Yahoo or other big name sites, I wanted to base my project around a site related to the things I enjoy. That being the case, I decided to choose ``WEBTOONS`` as it was a site centered around Art. It's a website that allows creators to post their very own webtoon(s) (a digital comic originating from Korea) with readers being able to read them worldwide.

## **Milestone 2: Obtaining a list of links to the required pages**
---

To begin this project, I needed to install a few dependencies that would aid me in automated web browising and data collection. Therefore, I first started off creating a new conda environment using the ``conda create -n web_scraper python=3.10`` command in VS Code. Then, using Python's included module, pip, I installed both Selenium and BeautifulSoup using the commands ``pip install selenium`` and ``pip install beautifulsoup4``. I then proceeded to download a webdriver that was compatible with my version of Chrome.

My main script was called ``run.py`` and contained all the methods needed to instantiate my web scraper. I used Object Oriented Programming for this project and ran the script using the ``if __name__ == "__main__"`` statement. The other files that contained all other classes and methods needed for this project were stored in a folder called 'modules'.

My first task was to load the main page of the website using selenium. I initialised a class called 'Webtoon' which would store all my methods needed to run this web scraper. I used the ``.get()`` method to load the main page which redirected me to an age verification page. Using the ``.find_element(By.XPATH, 'your_path')`` and ``send_keys()`` functions I was able to pass a date of 24/10/1998 into the relevant fields and click continue to bypass the age gate.

This brought me to the actual main page where I was greeted with cookies. To get past this I created a 'load_and_accept_cookies' method which found the cookies frame using XPATH and clicked on the 'I Agree' button. However, to make my code more robust by taking into account load time and other factors, I used the ``expected_conditions`` module from selenium to wait a minimum of 10 sec for the element to load. If successful it would continue through the rest of my code but if it ran into a TimeoutException error it would print a message in the terminal.

To start scraping relevant data from the website, I decided to use the 'Genres' tab to find all the webtoons currently available on the website. I created a new file called 'genres.py' and used it to store a class that would solely be used to scrape both genre and webtoon link data. Using the By.XPATH, By.CLASS_NAME and By.TAG_NAME methods from selenium I was able to located the genres available and stored them in a list for future use. I then proceeded to use the same functions to scrape the links to every webtoon and stored them in a dictionary.

## **Milestone 3: Retrieveing relevant data from all pages**
---
## **Milestone 4: Documenting and unit testing**
---
## **Milestone 5: Scalably storing the data**
---
## **Milestone 6: Preventing re-scraping and getting more data**
---
## **Milestone 7: Containerising the scraper and running it on a cloud server**
---
## **Milestone 8: Monitering and alerting**
---
## **Milestone 9: Setting up a CI/CD pipeline for your Docker image**
---