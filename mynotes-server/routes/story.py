import datetime
from flask import Blueprint, request, jsonify
from neo4j_db import add_category_to_story, add_story_to_user, create_categories, \
    create_story, get_all_categories, get_db, create_category,\
    get_story_by_id, serialize_category, serialize_story, \
    serialize_user, get_user_by_id, get_latest_stories, get_latest_stories_by_category,\
    remove_story_from_category, update_story, delete_story
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token

story_route = Blueprint("story", __name__)

@story_route.route("/story/get-categories", methods=["GET"])
def get_categories():
    #create_categories()
    db = get_db()
    categories_record = db.read_transaction(get_all_categories)

    all_categories = []
    for cat in categories_record:
        all_categories.append(cat['c'])

    return jsonify({'categories': [serialize_category(x) for x in all_categories]}), 201

@story_route.route("/story/get-story", methods=["GET"])
def get_story_bid():
    db = get_db()
    story_id = request.args.get('id')
    story_record = db.read_transaction(get_story_by_id, story_id)
    
    story = story_record[0]['story']
    category = story_record[0]['c']
    writer = story_record[0]['u']

    return jsonify({'story': serialize_story(story, writer, category)}), 201

@story_route.route("/story/create-story", methods=["POST"])
@jwt_required()
def create_new_story():
    req = request.get_json()

    title = str(req["title"])
    text = str(req["text"])
    category_id = str(req["category"])

    db = get_db()

    writer = get_jwt_identity()

    # TEST #
    # writer_id = "cf2e70cc-d0cf-47e5-91e4-7014c015b6bc"
    # writer = db.read_transaction(get_user_by_id, writer_id)

    new_story = db.write_transaction(create_story, title, text, 0.0, datetime.datetime.now())

    db.write_transaction(add_category_to_story, new_story[0]['id'], category_id)
    db.write_transaction(add_story_to_user, writer, new_story[0]['id'])

    return jsonify({'msg':'ok MILICA JE LIVRA'}), 201

@story_route.route("/story/get-latest-stories", methods=["GET"])
def get_lts_stories():
    page = int(request.args.get('page'))
    limit = 5
    db = get_db()

    record = db.read_transaction(get_latest_stories, page*limit, limit)

    all_stories = []
    for r in record:
        obj = {
            'story': r['story'],
            'writer': r['u'],
            'category': r['c']
        }
        all_stories.append(obj)
    
    return jsonify({'stories': [serialize_story(x['story'], x['writer'], x['category']) for x in all_stories]}), 201


@story_route.route("/story/get-latest-by-cat", methods=["GET"])
def get_by_cat():
    page = int(request.args.get('page'))
    category_id = str(request.args.get('categoryId'))

    limit = 5
    db = get_db()

    record = db.read_transaction(get_latest_stories_by_category, category_id, page*limit, limit)

    all_stories = []
    for r in record:
        obj = {
            'story': r['story'],
            'writer': r['u'],
            'category': r['c']
        }
        all_stories.append(obj)
    
    return jsonify({'stories': [serialize_story(x['story'], x['writer'], x['category']) for x in all_stories]}), 201

@story_route.route("/story/update-story", methods=["PATCH", "UPDATE"])
def update_st():
    req = request.get_json()

    updated_story = req

    db = get_db()

    db_result = db.read_transaction(get_story_by_id, updated_story['id'])
    story_from_db = db_result[0]['story']
    category_from_db = db_result[0]['c']
    writer_from_db = db_result[0]['u']

    if writer_from_db['id'] != updated_story['writer']['id']:
        return jsonify({'error': 'Permission denied'}), 101

    if category_from_db['id'] != updated_story['category']['id']:
        db.write_transaction(remove_story_from_category, story_from_db['id'], category_from_db['id'])
        db.write_transaction(add_category_to_story, story_from_db['id'], updated_story['category']['id'])

    db.write_transaction(update_story, updated_story['id'], updated_story['title'], updated_story['text'])
    
    return jsonify({'message': 'OK'}), 201

@story_route.route('/story/delete-story', methods=["DELETE"])
def del_st():
    story_id = str(request.args.get('id'))

    db = get_db()

    db.write_transaction(delete_story, story_id)

    return jsonify({'message': 'OK'}), 201