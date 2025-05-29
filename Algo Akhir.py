import webbrowser
import os

file_path = os.path.abspath("peta.html")
webbrowser.open(f"file://{file_path}")