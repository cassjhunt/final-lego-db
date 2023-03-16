import psycopg2
from flask import Flask, request, render_template, redirect, url_for, request
from psycopg2.extras import RealDictCursor
import math


from sets import search_sets, count_sets, add_favorite, SORT_BY_PARAMS, SORT_DIR_PARAMS
from favorites import search_favorites, count_favorites
from util import safe_int, within_valid_values

conn = psycopg2.connect(
    "host=db dbname=postgres user=postgres password=postgres",
    cursor_factory=RealDictCursor)
app = Flask(__name__)

# TODO: create /sets HTML endpoint


@app.route('/sets/add-fav', methods=["POST"])
def add_favorite_set():
    set_num = request.form['set_num']
    with conn.cursor() as cur:
        add_favorite(cur, set_num)
        print("added fav: ", set_num)
    return redirect(location='/sets', code=302)


@app.route('/sets/favorites')
def favorite_sets_html():
    set_name = request.args.get('set_name', '')
    theme_name = request.args.get('theme_name', '')
    part_count_gte = safe_int(request.args.get('part_count_gte'), 0)
    part_count_lte = safe_int(request.args.get('part_count_lte'), 999999)
    sort_by = within_valid_values(request.args.get(
        'sort_by'), SORT_BY_PARAMS, 'set_num')
    sort_dir = within_valid_values(
        request.args.get('sort_dir'), SORT_DIR_PARAMS, 'asc')
    page = safe_int(request.args.get('page'), 1)
    limit = safe_int(request.args.get('limit'), 50)
    favorite = request.args.get('favorite', False)
    # TODO: all the other params
    offset = (page-1) * limit

    with conn.cursor() as cur:
        count = count_favorites(cur, set_name_contains=set_name,
                                theme_name_contains=theme_name, part_count_gte=part_count_gte, part_count_lte=part_count_lte)
        results = search_favorites(cur, set_name_contains=set_name, theme_name_contains=theme_name, part_count_gte=part_count_gte, part_count_lte=part_count_lte,
                                   limit=limit, offset=offset, favorite=True, sort_by=sort_by, sort_dir=sort_dir)
        page_count = math.ceil(count / limit) + 1
        return render_template('favorites.html', count=count, results=results, set_name=set_name, theme_name=theme_name, part_count_gte=part_count_gte, part_count_lte=part_count_lte, page=page, sort_by=sort_by, sort_dir=sort_dir, num_pages=page_count, limit=limit)


@app.route('/sets')
def search_sets_html():
    set_name = request.args.get('set_name', '')
    theme_name = request.args.get('theme_name', '')
    part_count_gte = safe_int(request.args.get('part_count_gte'), 0)
    part_count_lte = safe_int(request.args.get('part_count_lte'), 999999)
    sort_by = within_valid_values(request.args.get(
        'sort_by'), SORT_BY_PARAMS, 'set_num')
    sort_dir = within_valid_values(
        request.args.get('sort_dir'), SORT_DIR_PARAMS, 'asc')
    page = safe_int(request.args.get('page'), 1)
    limit = safe_int(request.args.get('limit'), 50)
    favorite = request.args.get('favorite', False)
    # TODO: all the other params
    offset = (page-1) * limit

    with conn.cursor() as cur:
        count = count_sets(cur, set_name_contains=set_name,
                           theme_name_contains=theme_name, part_count_gte=part_count_gte, part_count_lte=part_count_lte)
        results = search_sets(cur, set_name_contains=set_name, theme_name_contains=theme_name, part_count_gte=part_count_gte, part_count_lte=part_count_lte,
                              limit=limit, offset=offset, sort_by=sort_by, sort_dir=sort_dir)
        page_count = math.ceil(count / limit) + 1
        return render_template('sets.html', count=count, results=results, set_name=set_name, theme_name=theme_name, part_count_gte=part_count_gte, part_count_lte=part_count_lte, page=page, sort_by=sort_by, sort_dir=sort_dir, num_pages=page_count, limit=limit)
