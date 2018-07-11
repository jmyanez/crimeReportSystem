# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


builtin_list = list


db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255))
    date = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    # imageUrl = db.Column(db.String(255))
    crime = db.Column(db.String(4096))
    createdBy = db.Column(db.String(255))
    createdById = db.Column(db.String(255))

    def __repr__(self):
        return "<Report(crime='%s', gender=%s)" % (self.crime, self.gender)


def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Report.query
             .order_by(Report.title)
             .limit(limit)
             .offset(cursor))
    reports = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(reports) == limit else None
    return (reports, next_page)


def list_by_user(user_id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Report.query
             .filter_by(createdById=user_id)
             .order_by(Report.title)
             .limit(limit)
             .offset(cursor))
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)


def read(id):
    result = Report.query.get(id)
    if not result:
        return None
    return from_sql(result)


def create(data):
    report = Report(**data)
    db.session.add(report)
    db.session.commit()
    return from_sql(report)


def update(data, id):
    report = Report.query.get(id)
    for k, v in data.items():
        setattr(report, k, v)
    db.session.commit()
    return from_sql(report)


def delete(id):
    Report.query.filter_by(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
