from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import sqlite3

app = Flask(__name__)
CORS(app, origins="*")

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('recipes.db')
    df = pd.read_sql_query('SELECT * FROM users LIMIT 1000', conn)
    conn.close()
    return jsonify({'success': True, 'users': df.to_dict(orient='records')})

@app.route('/api/pp_recipes', methods=['GET'])
def get_pp_recipes():
    conn = sqlite3.connect('recipes.db')
    df = pd.read_sql_query('SELECT * FROM pp_recipes LIMIT 1000', conn)
    conn.close()
    return jsonify({'success': True, 'pp_recipes': df.to_dict(orient='records')})

@app.route('/api/interactions', methods=['GET'])
def get_interactions():
    conn = sqlite3.connect('recipes.db')
    df = pd.read_sql_query('SELECT * FROM interactions LIMIT 1000', conn)
    conn.close()
    return jsonify({'success': True, 'interactions': df.to_dict(orient='records')})

@app.route('/api/recipes/search', methods=['GET'])
def search_recipes():
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    # Основные фильтры
    name = request.args.get('name')
    min_minutes = request.args.get('min_minutes')
    max_minutes = request.args.get('max_minutes')
    min_ingredients = request.args.get('min_ingredients')
    max_ingredients = request.args.get('max_ingredients')
    min_calories = request.args.get('min_calories')
    max_calories = request.args.get('max_calories')
    
    # Фильтры по категориям
    meal_types = request.args.get('meal_types')
    cuisines = request.args.get('cuisines')
    diets = request.args.get('diets')
    methods = request.args.get('methods')
    occasions = request.args.get('occasions')
    seasons = request.args.get('seasons')
    difficulties = request.args.get('difficulties')
    ingredients = request.args.get('ingredients')
    desserts_sweets = request.args.get('desserts_sweets')
    beverages = request.args.get('beverages')
    meat_seafood = request.args.get('meat_seafood')
    
    # Новые фильтры
    time_preparation = request.args.get('time_preparation')
    dietary_restrictions = request.args.get('dietary_restrictions')
    breads_baking = request.args.get('breads_baking')
    special_occasions = request.args.get('special_occasions')

    query = '''SELECT * FROM recipes WHERE 1=1'''
    params = {}
    
    # 🔍 ПОИСК ПО НАЗВАНИЮ
    if name:
        query += ' AND LOWER(name) LIKE :name'
        params['name'] = f'%{name.lower()}%'
    
    # ⏱️ ФИЛЬТРЫ ПО ВРЕМЕНИ ПРИГОТОВЛЕНИЯ
    if min_minutes:
        query += ' AND minutes >= :min_minutes'
        params['min_minutes'] = int(min_minutes)
    if max_minutes:
        query += ' AND minutes <= :max_minutes'
        params['max_minutes'] = int(max_minutes)
    
    # 🛒 ФИЛЬТРЫ ПО КОЛИЧЕСТВУ ИНГРЕДИЕНТОВ
    if min_ingredients:
        query += ' AND n_ingredients >= :min_ingredients'
        params['min_ingredients'] = int(min_ingredients)
    if max_ingredients:
        query += ' AND n_ingredients <= :max_ingredients'
        params['max_ingredients'] = int(max_ingredients)
    
    # 🔥 ФИЛЬТРЫ ПО КАЛОРИЯМ (nutrition: первое значение)
    if min_calories:
        query += " AND CAST(SUBSTR(nutrition, 1, INSTR(nutrition, ',' )-1) AS REAL) >= :min_calories"
        params['min_calories'] = float(min_calories)
    if max_calories:
        query += " AND CAST(SUBSTR(nutrition, 1, INSTR(nutrition, ',' )-1) AS REAL) <= :max_calories"
        params['max_calories'] = float(max_calories)
    
    # 🏷️ ФИЛЬТРЫ ПО КАТЕГОРИЯМ (ТЕГАМ)
    def add_multi_like(param_value, param_name):
        if param_value:
            values = [v.strip() for v in param_value.split(',') if v.strip()]
            conditions = []
            for idx, v in enumerate(values):
                qname = f'{param_name}_{idx}'
                conditions.append(f"tags LIKE :{qname}")
                params[qname] = f'%,{v},%'
            if conditions:
                nonlocal query
                query += ' AND (' + ' OR '.join(conditions) + ')'
    
    # Применяем фильтры по категориям
    add_multi_like(meal_types, 'meal_types')
    add_multi_like(cuisines, 'cuisines')
    add_multi_like(diets, 'diets')
    add_multi_like(methods, 'methods')
    add_multi_like(occasions, 'occasions')
    add_multi_like(seasons, 'seasons')
    add_multi_like(difficulties, 'difficulties')
    add_multi_like(ingredients, 'ingredients')
    add_multi_like(desserts_sweets, 'desserts_sweets')
    add_multi_like(beverages, 'beverages')
    add_multi_like(meat_seafood, 'meat_seafood')
    
    # Новые фильтры
    add_multi_like(time_preparation, 'time_preparation')
    add_multi_like(dietary_restrictions, 'dietary_restrictions')
    add_multi_like(breads_baking, 'breads_baking')
    add_multi_like(special_occasions, 'special_occasions')
    
    query += ' ORDER BY name LIMIT :limit OFFSET :offset'
    params['limit'] = limit
    params['offset'] = offset

    try:
        conn = sqlite3.connect('recipes.db')
        # Получаем рецепты с пагинацией
        df = pd.read_sql_query(query, conn, params=params)
        
        # Получаем общее количество найденных рецептов
        count_query = 'SELECT COUNT(*) as total FROM recipes WHERE 1=1'
        count_params = {}
        
        # Повторяем условия фильтрации для count
        if name:
            count_query += ' AND LOWER(name) LIKE :name'
            count_params['name'] = f'%{name.lower()}%'
        if min_minutes:
            count_query += ' AND minutes >= :min_minutes'
            count_params['min_minutes'] = int(min_minutes)
        if max_minutes:
            count_query += ' AND minutes <= :max_minutes'
            count_params['max_minutes'] = int(max_minutes)
        if min_ingredients:
            count_query += ' AND n_ingredients >= :min_ingredients'
            count_params['min_ingredients'] = int(min_ingredients)
        if max_ingredients:
            count_query += ' AND n_ingredients <= :max_ingredients'
            count_params['max_ingredients'] = int(max_ingredients)
        if min_calories:
            count_query += " AND CAST(SUBSTR(nutrition, 1, INSTR(nutrition, ',' )-1) AS REAL) >= :min_calories"
            count_params['min_calories'] = float(min_calories)
        if max_calories:
            count_query += " AND CAST(SUBSTR(nutrition, 1, INSTR(nutrition, ',' )-1) AS REAL) <= :max_calories"
            count_params['max_calories'] = float(max_calories)
            
        # Повторяем фильтры по тегам для count
        def add_count_multi_like(param_value, param_name):
            if param_value:
                values = [v.strip() for v in param_value.split(',') if v.strip()]
                conditions = []
                for idx, v in enumerate(values):
                    qname = f'count_{param_name}_{idx}'
                    conditions.append(f"tags LIKE :{qname}")
                    count_params[qname] = f'%,{v},%'
                if conditions:
                    nonlocal count_query
                    count_query += ' AND (' + ' OR '.join(conditions) + ')'
        
        add_count_multi_like(meal_types, 'meal_types')
        add_count_multi_like(cuisines, 'cuisines')
        add_count_multi_like(diets, 'diets')
        add_count_multi_like(methods, 'methods')
        add_count_multi_like(occasions, 'occasions')
        add_count_multi_like(seasons, 'seasons')
        add_count_multi_like(difficulties, 'difficulties')
        add_count_multi_like(ingredients, 'ingredients')
        add_count_multi_like(desserts_sweets, 'desserts_sweets')
        add_count_multi_like(beverages, 'beverages')
        add_count_multi_like(meat_seafood, 'meat_seafood')
        add_count_multi_like(time_preparation, 'time_preparation')
        add_count_multi_like(dietary_restrictions, 'dietary_restrictions')
        add_count_multi_like(breads_baking, 'breads_baking')
        add_count_multi_like(special_occasions, 'special_occasions')
        
        count_df = pd.read_sql_query(count_query, conn, params=count_params)
        total_count = int(count_df['total'].iloc[0]) if not count_df.empty else 0
        
        conn.close()
        
        # Обеспечиваем наличие description
        if 'description' not in df.columns:
            df['description'] = ''
            
        return jsonify({
            'success': True,
            'recipes': df.to_dict(orient='records'),
            'total': total_count
        })
    except Exception as e:
        print(f"DEBUG: Database error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'recipes': [],
            'total': 0
        }), 500
        
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    query = 'SELECT * FROM recipes WHERE 1=1'
    params = {}
    
    # ФИЛЬТР: фильтрация по тегам
    tags = request.args.get('tags')
    print(f"DEBUG: Received tags parameter: {tags}")
    
    if tags:
        try:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            print(f"DEBUG: Parsed tag list: {tag_list}")
            
            if tag_list:
                tag_conditions = []
                for i, tag in enumerate(tag_list):
                    param_name = f'tag_{i}'
                    tag_conditions.append(f"tags LIKE :{param_name}")
                    params[param_name] = f'%,{tag},%'
                
                if tag_conditions:
                    query += ' AND (' + ' OR '.join(tag_conditions) + ')'
        except Exception as e:
            print(f"DEBUG: Error parsing tags: {e}")
            return jsonify({
                'success': False,
                'error': f'Error parsing tags: {str(e)}',
                'recipes': [],
                'total': 0
            }), 400
    
    # Простая пагинация
    query += ' ORDER BY name LIMIT :limit OFFSET :offset'
    params['limit'] = limit
    params['offset'] = offset

    print(f"DEBUG: Final query: {query}")
    print(f"DEBUG: Query params: {params}")

    try:
        conn = sqlite3.connect('recipes.db')
        
        # Получаем рецепты с пагинацией
        df = pd.read_sql_query(query, conn, params=params)
        print(f"DEBUG: Found {len(df)} recipes")
        
        # УПРОЩЕННЫЙ ПОДСЧЕТ: делаем отдельный запрос для подсчета
        count_query = 'SELECT COUNT(*) as total FROM recipes WHERE 1=1'
        count_params = {}
        
        # Повторяем условия фильтрации для count
        if tags:
            try:
                tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
                if tag_list:
                    tag_conditions = []
                    for i, tag in enumerate(tag_list):
                        param_name = f'count_tag_{i}'
                        tag_conditions.append(f"tags LIKE :{param_name}")
                        count_params[param_name] = f'%,{tag},%'
                    
                    if tag_conditions:
                        count_query += ' AND (' + ' OR '.join(tag_conditions) + ')'
            except Exception as e:
                print(f"DEBUG: Error in count query: {e}")
        
        count_df = pd.read_sql_query(count_query, conn, params=count_params)
        total_count = int(count_df['total'].iloc[0]) if not count_df.empty else 0
        print(f"DEBUG: Total count: {total_count}")
        
        conn.close()
        
        # Обеспечиваем наличие description
        if 'description' not in df.columns:
            df['description'] = ''
            
        return jsonify({
            'success': True,
            'recipes': df.to_dict(orient='records'),
            'total': total_count
        })
    except Exception as e:
        print(f"DEBUG: Database error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'recipes': [],
            'total': 0
        }), 500

    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    query = 'SELECT * FROM recipes WHERE 1=1'
    params = {}
    
    # НОВЫЙ ФИЛЬТР: фильтрация по тегам
    tags = request.args.get('tags')
    print(f"DEBUG: Received tags parameter: {tags}")  # Добавим отладку
    
    if tags:
        try:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            print(f"DEBUG: Parsed tag list: {tag_list}")  # Отладка
            
            if tag_list:
                tag_conditions = []
                for i, tag in enumerate(tag_list):
                    param_name = f'tag_{i}'
                    tag_conditions.append(f"tags LIKE :{param_name}")
                    params[param_name] = f'%,{tag},%'
                
                if tag_conditions:
                    query += ' AND (' + ' OR '.join(tag_conditions) + ')'
                    print(f"DEBUG: Final query condition: {tag_conditions}")  # Отладка
        except Exception as e:
            print(f"DEBUG: Error parsing tags: {e}")
            return jsonify({
                'success': False,
                'error': f'Error parsing tags: {str(e)}',
                'recipes': [],
                'total': 0
            }), 400
    
    # Простая пагинация
    query += ' ORDER BY name LIMIT :limit OFFSET :offset'
    params['limit'] = limit
    params['offset'] = offset

    print(f"DEBUG: Final query: {query}")  # Отладка
    print(f"DEBUG: Query params: {params}")  # Отладка

    try:
        conn = sqlite3.connect('recipes.db')
        # Получаем рецепты с пагинацией
        df = pd.read_sql_query(query, conn, params=params)
        print(f"DEBUG: Found {len(df)} recipes")  # Отладка
        
        # Получаем общее количество рецептов (упростим для отладки)
        count_query = query.replace('ORDER BY name LIMIT :limit OFFSET :offset', '')
        count_query = f"SELECT COUNT(*) as total FROM ({count_query})"
        
        count_df = pd.read_sql_query(count_query, conn, params=params)
        total_count = int(count_df['total'].iloc[0]) if not count_df.empty else 0
        print(f"DEBUG: Total count: {total_count}")  # Отладка
        
        conn.close()
        
        # Обеспечиваем наличие description
        if 'description' not in df.columns:
            df['description'] = ''
            
        return jsonify({
            'success': True,
            'recipes': df.to_dict(orient='records'),
            'total': total_count
        })
    except Exception as e:
        print(f"DEBUG: Database error: {e}")  # Отладка
        return jsonify({
            'success': False,
            'error': str(e),
            'recipes': [],
            'total': 0
        }), 500
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    # To DO: Добавить фильтры позже
    query = 'SELECT * FROM recipes WHERE 1=1'
    params = {}
    
    # НОВЫЙ ФИЛЬТР: фильтрация по тегам
    tags = request.args.get('tags')
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        if tag_list:
            tag_conditions = []
            for i, tag in enumerate(tag_list):
                param_name = f'tag_{i}'
                tag_conditions.append(f"tags LIKE :{param_name}")
                params[param_name] = f'%,{tag},%'
            
            if tag_conditions:
                query += ' AND (' + ' OR '.join(tag_conditions) + ')'
    
    # Простая пагинация
    query += ' ORDER BY name LIMIT :limit OFFSET :offset'
    params['limit'] = limit
    params['offset'] = offset

    try:
        conn = sqlite3.connect('recipes.db')
        # Получаем рецепты с пагинацией
        df = pd.read_sql_query(query, conn, params=params)
        
        # Получаем общее количество рецептов
        count_query = 'SELECT COUNT(*) as total FROM recipes WHERE 1=1'
        count_params = params.copy()
        # Удаляем LIMIT/OFFSET для count
        for k in ['limit', 'offset']:
            if k in count_params:
                del count_params[k]
        # Повторяем все фильтры
        count_query += query[query.find('AND'):] if 'AND' in query else ''
        count_df = pd.read_sql_query(count_query, conn, params=count_params)
        total_count = int(count_df['total'].iloc[0]) if not count_df.empty else 0
        
        conn.close()
        
        # Обеспечиваем наличие description
        if 'description' not in df.columns:
            df['description'] = ''
            
        return jsonify({
            'success': True,
            'recipes': df.to_dict(orient='records'),
            'total': total_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'recipes': [],
            'total': 0
        }), 500
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    conn = sqlite3.connect('recipes.db')
    df = pd.read_sql_query('SELECT * FROM recipes LIMIT 10', conn)
    conn.close()
    if 'description' not in df.columns:
        df['description'] = ''
    return jsonify({'success': True, 'recipes': df.to_dict(orient='records')})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    # Логика регистрации (заглушка)
    return jsonify({"success": True})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'success': True, 'status': 'API is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)