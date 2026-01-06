# LyFy

> [!WARNING]
> Cool relic from the past straight to archive.

A Python WebScraper to show the lyrics of the song being played on Spotify.

It uses *dbus* library in python to access the Spotify session and asks it for the songs' info.

The info is then passed on to *Selenium* WebDriver (GhostDriver) to search the query on AZLyrics and return the first result (generally acceptable) along the lyrics.

The UI is made in two Python libraries - *Gtk* and *Tkinter* - separately.
