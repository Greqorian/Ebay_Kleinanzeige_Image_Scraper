
<!-- PROJECT LOGO -->
<br />
<p align="center">
![ebay_images](batch_ebay_images.png)
  <h3 align="center">Ebay_Kleinanzeige_Image_Scraper</h3>

  <p align="center">
    Scraping pictures from Ebay Kleinanzige websites
  </p>
</p>


<!-- ABOUT THE PROJECT -->
### About The Project

This script was developed as part of a bachelor thesis at HTW Berlin.
It allows to collect image files from ebay-kleinanzeigen.de website in order to train an artificial intelligence model to recognize ikea store products. 
The model used in the IKEA_classifier application is part of the final project.

### How to use

To start collecting images from the ikea website, please open the jupiter notebook in [Google Colab](https://colab.research.google.com/drive/1hOcuZJ_1B5fV5EHMvxtlfyTGhy_meC1z?usp=sharing) and follow the instructions

### Table of content
<br/> 1. Libraries and constants definition
<br/> 1.1 Import libraries
<br/> 1.2 Define headers to be visible as the Google Bot.
<br/> 1.3 Mount storage
<br/> 2. Function definition
<br/> 2.1 Create BeautifulSoup instance
<br/> 2.2 Creates a list of URL adresses in Ebay Kleinanzeige service of one item
<br/> 2.3 Create a list of images sources
<br/> 3. Execution
<br/> 3.1 Open a list of items
<br/> 3.2 Create a list of ebay items based of the list of items names
<br/> 3.4 Change directory to save the itemsList (optional)
<br/> 3.5 Save the list of IKEA Products to JSON file (optional)
<br/> 3.6 Set your train ditrectory to save download images 
<br/> 3.7 Scrape images to selected directory and create list of labels

### Built With

* [Google Colab](https://colab.research.google.com/)
* [Python](https://www.python.org/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)

<!-- CONTACT -->
### Contact

Gregor Pawlak - [linkedIn](https://www.linkedin.com/in/grzegorz-pawlak/) 

Project Link: [https://github.com/Greqorian/Ebay_Kleinanzeige_Image_Scraper](https://github.com/Greqorian/Ebay_Kleinanzeige_Image_Scraper)
