import webbrowser
import urllib.parse


class BrowserTools:

    @staticmethod
    def google_search(query):
        encoded = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded}"
        webbrowser.open(url)
        return f"Searching Google for: {query}"

    @staticmethod
    def open_youtube(query=None):

        if query:
            encoded = urllib.parse.quote(query)
            url = f"https://www.youtube.com/results?search_query={encoded}"
        else:
            url = "https://youtube.com"

        webbrowser.open(url)
        return "YouTube opened"