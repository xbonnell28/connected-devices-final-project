import datetime
import keen
from requests import ConnectionError


class KeenEventRecorder:
    def __init__(self, keen_project_id, keen_write_key):
        keen.project_id = keen_project_id
        keen.write_key = keen_write_key

    def record_event(self, collection, event_dict):
        e = self.build_default_keen_event()
        e.update(event_dict)
        keen.add_event(collection, e)

    def build_default_keen_event(self):
        return {
            'keen': {
                'timestamp': datetime.datetime.now().isoformat(),
                'addons': [
                    {
                        'name': 'keen:date_time_parser',
                        'input': {
                            'date_time': 'keen.timestamp',
                        },
                        'output': 'timestamp.info',
                    },
                ]
            },
            }
