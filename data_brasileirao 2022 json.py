import pandas as pd
import matplotlib.pyplot as plt
import json

from pathlib import Path

df_jogos = pd.read_json("datasets/only_matches_2022.json")

filepath = Path('out/jogos2022.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)  
df_jogos.to_csv(filepath)