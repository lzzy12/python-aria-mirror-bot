import requests
from bot import LOGGER

def search_torrent_link(query):
	LOGGER.info("Searching torrent on query")
	query = query.replace("/", "")
	try:
		r = requests.get(
        	"https://torrent-paradise.ml/api/search?q=" + query)
		torrents = r.json()
		torrents = sorted(torrents, key=lambda i: i['s'], reverse=True)
		torrent = torrents[0]
	except:
		return "not found"
	LOGGER.info("Torrent Found")
	reply = ""
	reply += "magnet:?xt=urn:btih:" + torrent['id']
	reply += "&tr=udp://tracker.coppersurfer.tk:6969/announce&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://tracker.leechers-paradise.org:6969/announce"
	return reply