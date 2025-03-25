import requests
import numpy as np
import pandas as pd
from githubAPI import loadAccessToken, getAccessToken
from time import sleep
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer

# Load GitHub token
loadAccessToken()
GITHUB_TOKEN = getAccessToken()  # Insira seu token aqui
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

REPO = "pandas-dev/pandas"

# Mapeamento de tecnologias para perfis
TECH_TO_PROFILE = {
    "Python": "Data Science",
    "Jupyter Notebook": "Data Science",
    "Matlab": "Data Science",
    "MATLAB": "Data Science",
    "Mathematica": "Data Science",
    "Terra": "Data Science",
    "Julia": "Data Science",
    "F#": "Data Science",
    "R": "Data Science",
    "SQL": "Backend",
    "Scala": "Backend",
    "Java": "Backend",
    "C++": "Backend",
    "Ruby": "Backend",
    "Rust": "Backend",
    "Lua": "Backend",
    "Haskell": "Backend",
    "HTML": "Frontend",
    "CSS": "Frontend",
    "TypeScript": "Frontend",
    "JavaScript": "Frontend",
    "CoffeeScript": "Frontend",
    "React": "Frontend",
    "SCSS": "Frontend",
    "Swift": "Mobile",
    "Kotlin": "Mobile",
    "Dart": "Mobile",
    "HCL": "DevOps",
    "Shell": "DevOps",
    "Dockerfile": "DevOps",
    "YAML": "DevOps",
    "Nix": "DevOps",
    "Batchfile": "DevOps",
    "Emacs Lisp": "DevOps",
    "CMake": "DevOps",
    "Meson": "DevOps",
    "Vim Script": "DevOps",
    "VimL": "DevOps"
}

# Função para obter contribuidores
def get_contributors():
    contributors = []
    page = 1
    while len(contributors) < 250:
        url = f"https://api.github.com/repos/{REPO}/contributors?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if not data:
                break 
            contributors.extend(data)
            page += 1
        else:
            break
    return contributors[:250]

# Função para obter tecnologias usadas por um usuário
def get_languages(user):
    url = f"https://api.github.com/users/{user}/repos"
    response = requests.get(url, headers=HEADERS)
    languages = set()

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            if "language" in repo and repo["language"]:
                languages.add(repo["language"])
    
    return list(languages)

# Obtendo lista de contribuidores
contributors = get_contributors()

# Coletando dados de cada desenvolvedor
devs_data = []
for contributor in contributors[:250]:
    user = contributor["login"]
    languages = get_languages(user)
    profile = max(set([TECH_TO_PROFILE.get(lang, "Desconhecido") for lang in languages]), key=[TECH_TO_PROFILE.get(lang, "Desconhecido") for lang in languages].count, default="Desconhecido")
    devs_data.append({"login": user, "languages": languages, "profile": profile})

df = pd.DataFrame(devs_data)

# Convertendo linguagens para variáveis numéricas
mlb = MultiLabelBinarizer()
print(df.head())
print(df.columns)
X = mlb.fit_transform(df["languages"])

# Convertendo perfis para valores numéricos
profile_mapping = {profile: idx for idx, profile in enumerate(set(df["profile"]))}
y = df["profile"].map(profile_mapping)

# Treinando o modelo RandomForest
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

df["predicted_profile"] = model.predict(X)
df.to_excel("developers_profiles.xlsx", index=False, engine="openpyxl")

print("Arquivo Excel gerado: developers_profiles.xlsx")