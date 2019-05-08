#!/usr/bin/env python
import shelve

character_data = shelve.open('character.db')
try:
    character_data['health'] = '100'
    character_data['attack'] = '10'
finally:
    character_data.close()
