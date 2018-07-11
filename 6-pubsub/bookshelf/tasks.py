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

import logging

from bookshelf import get_model, storage
from flask import current_app
from google.cloud import pubsub
import psq
import requests


# [START get_books_queue]
publisher_client = pubsub.PublisherClient()
subscriber_client = pubsub.SubscriberClient()


def get_reports_queue():
    project = current_app.config['PROJECT_ID']

    # Create a queue specifically for processing books and pass in the
    # Flask application context. This ensures that tasks will have access
    # to any extensions / configuration specified to the app, such as
    # models.
    return psq.Queue(
        publisher_client, subscriber_client, project,
        'reports', extra_context=current_app.app_context)
# [END get_books_queue]


# [START process_book]
