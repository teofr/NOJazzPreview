# NOJazzPreview

The idea behind this project is to scrape the New Orleans Jazz Fest site and create playlists for each day in Spotify, so you can get a preview of the artist's music.

If all you want is the playlists you can find them here https://open.spotify.com/user/1140253737

#### Disclaimer, 
This is an error-prone, synchronous script to get the job done. Nothing fancy.

### Configuration

run pip3 install requirements.txt

install a web driver for selenium, here are instructions http://selenium-python.readthedocs.io/installation.html#drivers
(tested with geckodriver)

### Usage

* Create an app on the Spotify Dev Dashboard (https://beta.developer.spotify.com/dashboard/applications)

* You'll need your username (your email), your client ID and your client secret (both found on the dashboard)

* When you run this, it will show you some instructions and an URL, follow them.

* When the process is finished, you should have your playlists created and the following files:
	
	* not_found.txt: will show you the artists not found on Spotify

	* rewrite.txt: will show you the artist found on Spotify, for every artist on the lineup
