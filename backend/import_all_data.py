import sqlite3
import pandas as pd
import os

data_dir = os.path.join(os.path.dirname(__file__), 'data')
db_path = os.path.join(os.path.dirname(__file__), 'recipes.db')

# 1. Создание базы и таблиц
conn = sqlite3.connect(db_path)
c = conn.cursor()

# USERS
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    u INTEGER PRIMARY KEY,
    techniques TEXT,
    items TEXT,
    n_items INTEGER,
    ratings TEXT,
    n_ratings INTEGER
)
''')

# RECIPES
c.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    minutes INTEGER,
    contributor_id INTEGER,
    submitted TEXT,
    tags TEXT,
    nutrition TEXT,
    n_steps INTEGER,
    steps TEXT,
    description TEXT,
    ingredients TEXT,
    n_ingredients INTEGER
)
''')

# PP_RECIPES
c.execute('''
CREATE TABLE IF NOT EXISTS pp_recipes (
    id INTEGER PRIMARY KEY,
    i INTEGER,
    name_tokens TEXT,
    ingredient_tokens TEXT,
    steps_tokens TEXT,
    techniques TEXT,
    calorie_level TEXT,
    ingredient_ids TEXT
)
''')

# INTERACTIONS
c.execute('''
CREATE TABLE IF NOT EXISTS interactions (
    user_id INTEGER,
    recipe_id INTEGER,
    date TEXT,
    rating REAL,
    review TEXT,
    u INTEGER,
    i INTEGER
)
''')

conn.commit()

# 2. Импорт данных
# USERS
users_path = os.path.join(data_dir, 'PP_users.csv')
if os.path.exists(users_path):
    users = pd.read_csv(users_path)
    users.to_sql('users', conn, if_exists='replace', index=False)


# RECIPES с обработкой tags
import ast
def clean_tags(tags):
    if pd.isna(tags):
        return ''
    if isinstance(tags, str):
        try:
            tags_list = ast.literal_eval(tags)
            if isinstance(tags_list, list):
                return ',' + ','.join(t.strip() for t in tags_list) + ','
            else:
                return ',' + tags.replace(' ', '') + ','
        except:
            return ',' + tags.replace(' ', '') + ','
    elif isinstance(tags, list):
        return ',' + ','.join(t.strip() for t in tags) + ','
    return ''

recipes_path = os.path.join(data_dir, 'RAW_recipes.csv')
if os.path.exists(recipes_path):
    recipes = pd.read_csv(recipes_path)
    if 'tags' in recipes.columns:
        recipes['tags'] = recipes['tags'].apply(clean_tags)
    recipes.to_sql('recipes', conn, if_exists='replace', index=False)

# PP_RECIPES
pp_recipes_path = os.path.join(data_dir, 'PP_recipes.csv')
if os.path.exists(pp_recipes_path):
    pp_recipes = pd.read_csv(pp_recipes_path)
    pp_recipes.to_sql('pp_recipes', conn, if_exists='replace', index=False)

# INTERACTIONS (RAW + train/val/test)
def import_interactions(filename, has_review=False):
    path = os.path.join(data_dir, filename)
    if os.path.exists(path):
        df = pd.read_csv(path)
        if not has_review:
            df['review'] = None
        df.to_sql('interactions', conn, if_exists='append', index=False)

import_interactions('RAW_interactions.csv', has_review=True)
import_interactions('interactions_train.csv')
import_interactions('interactions_test.csv')
import_interactions('interactions_validation.csv')

print('Импорт завершён!')
conn.close()
