# Scrapping Data of Indian Film Actors

This script scrapes data of Indian film actors using python and scrapy. It achieves this in the following steps:

1. Scrapes list of all the Indian film actors from wikipedia
2. Constructs URL to be searched on starsunfolded.com
3. Scrapes data and image from their profiles on starsunfolded.com/name-of-actor

Since not all profiles are present on the site, only 44% of the actors is scraped. The data is in `actors.csv` and the images are stored in `images/` folder. The image path can also be accessed via the `image_path` column.

<b> This is raw data. <b>