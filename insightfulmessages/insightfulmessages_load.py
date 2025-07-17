import json
from datetime import datetime
from typing import Type

from insightfulmessages import InsightfulMessage
from insightfulmessages import DicomContentLoad

class InsightfulMessageLoader:

    # map from content_type to function that loads that content type
    content_map = {
        'DCM': DicomContentLoad
    }

    def __init__(self, content_loaders : list | dict = []):

        if isinstance(content_loaders, dict):
            content_loaders = [content_loaders]

        # Load in custom content loading functions
        for i in content_loaders:
            InsightfulMessageLoader.content_map[i] = content_loaders[i]


    def execute(self, input: str | dict) -> InsightfulMessage:
        """Convert a string (or dict) to an InsightfulMessage"""

        if isinstance(input, str):
            try:
                input = json.loads(input)
            except json.decoder.JSONDecodeError:
                print("Could not read json")
                return(None)

        if not 'role' in input:
            raise ValueError(f'No role found')

        if not 'content' in input:
            raise ValueError(f'No content found')

        msg = InsightfulMessage(role=input['role'])
        ctype = input['content']['content_type']

        if not ctype in InsightfulMessageLoader.content_map.keys():
            print(f'Unknown content_type: {ctype}')
            print("Known types: "+",".join(InsightfulMessageLoader.content_map.keys()))
            return None

        msg.content = InsightfulMessageLoader.content_map[ctype](input['content'])
        if msg.content is None:
            return(None)
            
        return(msg)

def insightful_message_load(input: str | dict ):
    loader = InsightfulMessageLoader()
    return(loader.execute(input))


        