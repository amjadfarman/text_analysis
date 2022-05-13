import json
import os
import time
from config import Config
from subroutines.preprocessor import Preprocessor

d_exists = os.path.exists("data")
if not d_exists:
    os.makedirs("data")

cfg = Config()
if cfg.get_property(property_name="scrape"):
    from subroutines.speech_getter import SpeechGetter

    main_addr = cfg.get_property(property_name="main_address")
    speech_addrs = cfg.get_property(property_name="speech_addresses")
    interval = cfg.get_property(property_name="interval")

    speeches = list()

    speech_getter = SpeechGetter(main_addr=main_addr)

    for addr in speech_addrs:
        speeches.append(speech_getter.get(speech_path=addr))
        time.sleep(interval)

    with open (file="data/speeches.json", mode="w") as file_handle:
        json.dump(obj=speeches, fp=file_handle)

with open(file="data/speeches.json", mode="r") as file_handle:
    speeches = json.load(file_handle)



preprocessor = Preprocessor(dataset=speeches)
df = preprocessor.preprocess()
df.to_csv("data/resultant_table.csv")