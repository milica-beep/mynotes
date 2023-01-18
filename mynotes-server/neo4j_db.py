from asyncio.trsock import TransportSocket
import datetime
from tokenize import Number
import uuid
from neo4j import GraphDatabase, Session, Transaction, basic_auth
from flask import g
from passlib.hash import sha256_crypt

DATABASE_USERNAME = "neo4j"
DATABASE_PASSWORD = "admin"
DATABASE_URL = "bolt://localhost:7687"

driver = GraphDatabase.driver(
    DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
)

def get_db() -> Session:
    if not hasattr(g, "neo4j_db"):
        g.neo4j_db = driver.session()
    return g.neo4j_db


def close_db(error):
    if hasattr(g, "neo4j_db"):
        g.neo4j_db.close()


# users

def get_user_by_id(tx: Transaction, user_id:str):
    return tx.run(
        """
        MATCH (user:User {id: $user_id}) RETURN user
        """,
        {"user_id": user_id},
    ).single()

def create_user(tx: Transaction, name: str, lastname: str, email: str, password: str):
    return tx.run(
        """
        CREATE (user:User {id: $id, name: $name, lastname: $lastname, email: $email, password: $password}) RETURN user
        """,
        {
            "id": str(uuid.uuid4()),
            "name": name,
            "lastname": lastname,
            "email": email,
            "password": sha256_crypt.hash(password),
        },
    ).single()


def get_user_by_email(tx: Transaction, email: str):
    return tx.run(
        """
        MATCH (user:User {email: $email}) RETURN user
        """,
        {"email": email},
    ).single()


def check_password(user, password_candidate):
    if sha256_crypt.verify(password_candidate, user["password"]):
        return 1
    else:
        return 0

# stories

def get_latest_stories(tx: Transaction, skip_value: int, limit_value: int):
    return tx.run(
        """
        MATCH (u:User)-[wr:WROTE]-(story:Story)-[:IN_CATEGORY]-(c:Category) RETURN story, c, u
        ORDER BY story.timestamp DESC
        SKIP $skip_value
        LIMIT $limit_value
        """,
        {
            "skip_value": skip_value,
            "limit_value": limit_value
        }
    ).data()

def get_latest_stories_by_category(tx: Transaction, category_id: str, skip_value: int, limit_value: int):
    return tx.run(
        """
        MATCH (u:User)-[wr:WROTE]-(story:Story)-[:IN_CATEGORY]-(c:Category {id: $category_id}) RETURN story, c, u
        ORDER BY story.timestamp DESC
        SKIP $skip_value
        LIMIT $limit_value
        """,
        {
            "skip_value": skip_value,
            "limit_value": limit_value,
            "category_id": category_id
        }
    ).data()

def create_story(tx: Transaction, title: str, text: str, grade: float, timestamp: datetime):
    return tx.run(
        """
        CREATE (story:Story {id: $id, title: $title, text: $text, grade: $grade, timestamp: $timestamp}) RETURN story
        """,
        {"id": str(uuid.uuid4()),
         "title": title, 
         "text": text,
         "timestamp": timestamp, 
         "grade": grade},
    ).single()

def get_story_by_id(tx: Transaction, story_id: str):
    return tx.run(
        """
        MATCH (u:User)-[wr:WROTE]-(story:Story {id: $story_id})-[:IN_CATEGORY]-(c:Category) 
        RETURN story, c, u
        """,
        {"story_id": story_id},
    ).data()

def delete_story(tx: Transaction, story_id: str):
    return tx.run(
                '''
                MATCH (story:Story {id: $story_id})
                OPTIONAL MATCH(story) - [rel] - ()
                DELETE rel, story
                ''', {'story_id': story_id}
            )

def update_story(tx:Transaction, story_id:str, title: str, text: str):
    return tx.run(
        """
        MATCH (story:Story {id: $story_id})
        SET story.title = $title
        SET story.text = $text
        """,
        {"story_id": story_id, "title": title, "text": text},
    )

def add_category_to_story(tx: Transaction, story_id: str, category_id: str):
    return tx.run(
        """
                MATCH (story:Story {id: $story_id}),(category:Category {id: $category_id})
                MERGE (story)-[ic:IN_CATEGORY]->(category)
                RETURN story
                """,
        {"story_id": story_id, "category_id": category_id},
    ).single()

def remove_story_from_category(tx: Transaction, story_id: str, cat_id: str):
    return tx.run(
        """
                MATCH (story:Story {id: $story_id}),(category:Category {id: $category_id})
                MERGE (story)-[ic:IN_CATEGORY]->(category)
                DELETE ic
                """,
        {"story_id": story_id, "category_id": cat_id},
    )

def add_user_rating(tx: Transaction, user_id: str, story_id: str, rating):
    return tx.run(
        """
            MATCH (u:User {id: $user_id}),(s:Story {story_id: $story_id})
            MERGE (u)-[r:RATED]->(s)
            SET r.rating = $rating
            RETURN m
            """,
        {"user_id": user_id, "story_id": story_id, "rating": rating},
    ) # sta je bre ovo "m" u return proveri obavezno sta ovo vraca


def add_story_to_user(tx: Transaction, user_id: str, story_id: str):
    return tx.run(
        """
                MATCH (user:User {id: $user_id}),(story:Story {id: $story_id})
                MERGE (user)-[w:WROTE]->(story)
                RETURN user
                """,
        {"user_id": user_id, "story_id": story_id},
    ).single()

# categories

def create_category(tx: Transaction, category_name: str):
    return tx.run(
        """
        CREATE (category:Category {id: $id, name: $name}) RETURN category
        """,
        {"id": str(uuid.uuid4()), "name": category_name},
    ).single()

def get_category_by_id(tx: Transaction, category_id: str):
    return tx.run(
        """
        MATCH (category:Category {id: $category_id}) RETURN category
        """,
        {"category_id": category_id},
    ).single()

def get_all_categories(tx: Transaction):
    return tx.run(
        """
        MATCH (c:Category) RETURN c
        """
    ).data()

def create_categories():
    query1 = "CREATE (c:Category { id: $id, name: 'Action' })"
    query2 = "CREATE (c:Category { id: $id, name: 'Romance' })"
    query3 = "CREATE (c:Category { id: $id, name: 'Comedy' })"
    query4 = "CREATE (c:Category { id: $id, name: 'Kids' })"
    query5 = "CREATE (c:Category { id: $id, name: 'Fantasy' })"

    db = get_db()

    db.run(query1, {"id": str(uuid.uuid4())})
    db.run(query2, {"id": str(uuid.uuid4())})
    db.run(query3, {"id": str(uuid.uuid4())})
    db.run(query4, {"id": str(uuid.uuid4())})
    db.run(query5, {"id": str(uuid.uuid4())})

def serialize_story(story, writer, category):
    return {"id": story["id"], "title": story["title"], "text": story["text"],\
            "grade": story["grade"], "timestamp": str(story["timestamp"]), \
            "writer": writer, "category": category}

def serialize_category(category):
    return {"id": category["id"], "name": category["name"]}

def serialize_user(user):
    return {"id": user["id"], "name": user["name"], "lastname": user["lastname"], "email": user["email"]}

# def serialize_comment(comment):
#     return {
#         'id': comment['id'],
#         'text': comment['text'],
#         'userId': comment['user_id'],
#         'userFullname': comment['user_fullname']
#     }