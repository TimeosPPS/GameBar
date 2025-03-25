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

