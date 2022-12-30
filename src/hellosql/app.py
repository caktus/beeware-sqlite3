"""
My first application
"""
from pathlib import Path
from tempfile import mkdtemp

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import sqlite3
import urllib.request


class HelloSQL(toga.App):
    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        # download db

        dest = Path(mkdtemp()) / Path("Chinook_Sqlite.sqlite")
        url = "https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
        response = urllib.request.urlopen(url)
        dest.write_bytes(response.read())

        # query db
        con = sqlite3.connect(dest)
        cur = con.cursor()
        res = cur.execute("SELECT Name, Composer FROM Track ORDER BY Name")

        rows = []
        for row in res.fetchall():
            data = {
                "icon": toga.Icon("resources/hellosql.png"),
                "title": row[0],
                "subtitle": row[1],
            }
            rows.append(data)

        # display table
        left_container = toga.Box()
        table = toga.DetailedList(
            # headings=["ID", "Track Name"],
            data=rows,
            style=Pack(flex=1),
        )
        left_container.add(table)

        # right_content = toga.Box(style=Pack(direction=COLUMN))
        # right_content.add(
        #     toga.Button(
        #         "Hello world!",
        #         on_press=self.button_handler,
        #         style=Pack(padding=20),
        #     )
        # )
        # right_container = toga.ScrollContainer()
        # right_container.content = right_content

        # split = toga.SplitContainer()
        # split.content = [left_container, right_container]

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = left_container
        self.main_window.show()

    def button_handler(self, widget):
        print("button press")


def main():
    return HelloSQL()
