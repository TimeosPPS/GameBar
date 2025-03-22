from sqlalchemy import asc, desc
from flask import make_response, redirect, url_for

from app.db.models.data import GameBarDB

import uuid
def get_sorted_query(query, sort_by):
    if sort_by == 'descend':
        return query.order_by(desc(GameBarDB.rating))
    elif sort_by == 'ascend':
        return query.order_by(asc(GameBarDB.rating))
    return query

def get_user():
    user = str(uuid.uuid4())
    resp = make_response(redirect(url_for('main_page')))
    resp.set_cookie('user_id', user, max_age=30 * 24 * 60 * 60)
    return resp