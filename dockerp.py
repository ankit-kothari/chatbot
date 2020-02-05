import pandas as pd

data = pd.read_csv('./dialog_talk_agent.csv', engine='python', encoding='utf8')
print(data)