"""
Script that does all the major work
This gets the lyrics
"""
import re
import dbus
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.PhantomJS(executable_path="../browser/phantomjs")


def open_link(link):
    """
    Function to open the link
    Searching for the song
    """
    browser.get(link)
    try:
        target = browser.find_element(
            By.XPATH, "//td[@class='text-left visitedlyr']")
        to_click = target.find_element(By.TAG_NAME, 'a')
        lyric_page = to_click.get_attribute('href')
        return lyric_page
    except:
        return 'error'


def get_lyrics(link):
    """
    Function to go to the first choice on AZLyrics
    And fetch the lyrics
    """
    browser.get(link)
    title = browser.find_element(By.TAG_NAME, 'h1')

    wording = browser.find_element(
        By.XPATH, "//div[@class='ringtone']/following-sibling::div")

    lyrics = title.text + '\n\n' + wording.text
    return lyrics


def print_lyrics():
    """
    Display the fetched lyrics to the user
    """
    song_info = get_spotify_song_data()
    song_name = remove_braces(song_info['title'])
    song_name = song_name.lower()
    song_artist = song_info['artist']
    song_artist = song_artist.lower()
    songn = song_name.replace(" ", "+")
    songa = song_artist.replace(" ", "+")
    if 'mad world' in song_name:
        query = 'mad+world+gary+jules'
    elif 'run' in song_name and 'bts' == song_artist:
        query = 'run+run+bts'
    else:
        query = songn + '+' + songa
    print(query)
    link = "https://search.azlyrics.com/search.php?q=" + query
    link = open_link(link)
    special_case = ('advertisement', 'spotify')
    if song_name in special_case:
        lyrics = "Buy Spotify Premium"
    elif link == 'error':
        lyrics = "Lyrics not found on AZLyrics"
    else:
        lyrics = get_lyrics(link)
    return lyrics


def remove_braces(string):
    """
    Remove braces from song name
    like (ft. Alouette)
    """
    string = re.sub(r"\(.*\)", "", string)
    string = re.sub(r"\[.*\]", "", string)
    return string


def get_spotify_song_data():
    """
    Function to read the song
    being played on Spotify
    """
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object(
        "org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(
        spotify_bus, "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get(
        "org.mpris.MediaPlayer2.Player", "Metadata")
    title = metadata['xesam:title'].encode(
        'utf-8').decode('utf-8').replace("&", "&amp;")
    artist = metadata['xesam:artist'][0].encode(
        'utf-8').decode('utf-8').replace("&", "&amp;")
    if '&amp;' in title:
        title = title.replace("&amp;", "%26")
    if '&amp;' in artist:
        artist = artist.replace("&amp;", "%26")
    return {'title': title, 'artist': artist}
