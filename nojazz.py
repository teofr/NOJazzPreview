from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import spotipy
import spotipy.util as util
import sys

if (len(sys.argv) != 4):
	print("Wrong number of arguments.\nUSAGE:")
	print("python3 nojazz.py <username> <client_id> <client_secret>")
	exit()

username = sys.argv[1]
client_id = sys.argv[2]
client_secret = sys.argv[3]


not_found = open("not_found.txt", mode='w')
rewrite = open("rewrite.txt", mode='w')

days  = ["{}-april-{}".format(x,y) for (x,y) in [('friday', 27), ('saturday', 28), ('sunday', 29)]]
days += ["{}-may-{}".format(x,y) for (x,y) in [('thursday', 3), ('friday', 4), ('saturday', 5), ('sunday', 6)]]

whole = {}

for day in days:
	driver = webdriver.Firefox()
	driver.get('http://www.nojazzfest.com/lineup/#/lineup_groupings/{}'.format(day))
	print(day)


	elements = driver.find_elements_by_class_name("ds-artist-name")

	artists = []
	for e in elements:
		artists.append(e.text)

	whole[day] = artists

	driver.close()


scope = 'user-library-read playlist-modify-public playlist-modify-private'

token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri='http://localhost/')

if token:
	sp = spotipy.Spotify(auth=token)
	user_id = sp.current_user()['id']
	user_playlists = sp.user_playlists(user_id, limit=50)

	for day in days:
		not_found.write(day + "\n\n")
		rewrite.write(day + "\n\n")

		for pl in user_playlists['items']:
			if "NOJazzDaily - {}".format(day) == pl['name']:
				sp.user_playlist_unfollow(user_id, pl['id'])

		playlist_id = sp.user_playlist_create(user_id, "NOJazzDaily - {}".format(day), public=True)['id']#, description='The Daily playlist for the New Orleans Jazz Fest ({})'.format(day))['id']

		for artist in whole[day]:
			result = sp.search(artist, limit=1, type='artist')
			if not result['artists']['items']:
				not_found.write(artist + '\n')
				continue

			artist_id = result['artists']['items'][0]['id']

			top_tracks = sp.artist_top_tracks(artist_id)
			tracks_ids = [track['id'] for track in top_tracks['tracks']]
			
			if not tracks_ids:
				not_found.write("*{}\n".format(artist))
				continue
			
			sp.user_playlist_add_tracks(user_id, playlist_id, tracks_ids[:5])
			
			#print("{} => {}".format(artist, result['artists']['items'][0]['name']))
			rewrite.write("{} => {}\n".format(artist, result['artists']['items'][0]['name']))

		not_found.write("\n\n")
		rewrite.write("\n\n")


else:
    print ("Can't get token for", username)