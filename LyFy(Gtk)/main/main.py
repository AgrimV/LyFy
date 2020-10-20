"""
Script to display the
lyrics to the user
"""
from gi.repository import Gtk
import lyfy
import platform
import os


class LyricWindow(Gtk.Window):
    """
    The window to display the lyrics
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="LyFy")

        self.current_song = lyfy.get_spotify_song_data()['title']
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_from_file("./icon/lyrics.png")
        self.set_default_size(350, 250)

        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox.set_homogeneous(False)
        vbox_up = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox_up.set_homogeneous(False)
        vbox_down = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox_down.set_homogeneous(False)
        hbox_up = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        vbox_down.pack_end(hbox_up, False, False, 0)

        btn1 = Gtk.Button(label='Reload')
        btn1.connect("clicked", self.refresh)
        hbox_up.pack_start(btn1, True, False, 50)

        btn2 = Gtk.Button(label='Save')
        btn2.connect("clicked", self.save)
        hbox_up.pack_end(btn2, True, False, 50)

        self.lyr = lyfy.print_lyrics()
        label = Gtk.Label(self.lyr)
        label.set_alignment(0.1, 0)
        vbox_up.pack_start(label, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(vbox_up)

        vbox.pack_start(scroll, True, True, 0)
        vbox.pack_start(vbox_down, False, False, 10)

        self.add(vbox)

    def refresh(self, widget):
        """
        Reload the lyrics
        """
        if not lyfy.get_spotify_song_data()['title'] == self.current_song:
            main()

    def save(self, widget):
        """
        Save the lyrics to /home/user/saved
        """
        name = lyfy.get_spotify_song_data()['title']
        if platform.system() == 'Linux':
            home = os.environ['HOME']
            os.system('mkdir $HOME/saved')
            with open(home + '/saved/' + name + '.txt', 'w') as file:
                file.write(self.lyr)
        else:
            os.system('mkdir ./saved')
            with open('./saved/' + name, 'w') as file:
                file.write(self.lyr)

def main():
    root = LyricWindow()
    root.connect("destroy", Gtk.main_quit)
    root.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
