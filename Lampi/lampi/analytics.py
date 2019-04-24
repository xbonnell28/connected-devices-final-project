import datetime
import platform
import Queue
import keen
from requests import ConnectionError
import threading


class KeenEventRecorder:
    def __init__(self, keen_project_id, keen_write_key, device_id):
        keen.project_id = keen_project_id
        keen.write_key = keen_write_key
        self._device_id = device_id
        self._keen_queue = Queue.Queue()
        self._keen_thread = threading.Thread(target=self._transmit_event)
        self._keen_thread.daemon = True
        self._keen_thread.start()

    def record_event(self, collection, event_dict):
        e = self.build_default_keen_event()
        e.update(event_dict)
        self._keen_queue.put((collection, e))

    def _transmit_event(self):
        # our thread method
        while 1:
            # block indefinitely until we get an item
            c, e = self._keen_queue.get(True, None)
            try:
                keen.add_event(c, e)
            except ConnectionError:
                # we cannot reach the internet, so drop the event
                pass

    def build_default_keen_event(self):
        return {
            'ip_address': '${keen.ip}',
            'tech': {
                'info': {
                    'device': {
                        'family': 'lampi',
                        'hardware_version': '1.0.0',
                        'firmware_version': '1.0.0',
                        'python_version': platform.python_version(),
                    },
                    'os': {
                        'family': platform.system(),
                        'platform': platform.platform(),
                    }
                }
            },
            'lampi': {
                'device_id': self._device_id,
                'ui': 'lampi',
            },
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
                    {
                        'name': 'keen:ip_to_geo',
                        'input': {
                            'ip': 'ip_address',
                        },
                        'output': 'geo',
                    },
                ]
            },
            }
