import requests
from bs4 import BeautifulSoup


class SpeechGetter:
    def __init__(self, main_addr: str) -> None:
        self.main_addr = main_addr

    def get(self, speech_path: str):
        full_path = f"{self.main_addr}/{speech_path}"
        title = ""
        speech = ""
        try:
            r = requests.get(full_path)
            soup = BeautifulSoup(r.content, "html.parser")
            title = soup.find('title').string.strip()
            body_soup = soup.find(name="main").find(name="div", attrs={"class": "section"})
            children = list(body_soup.children)
            for c in children:
                c_text = c.get_text().strip()
                if c_text != "":
                    speech += f" {c.get_text().strip()}"
        except Exception as e:
            print(f"The speech with address {speech_path} could not be fetched:\n{str(e)}")
        return {
            "title": title,
            "speech": speech,
            }