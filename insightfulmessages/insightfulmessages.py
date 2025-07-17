import json
from datetime import datetime
from typing import Union

class InsightfulMessageContent:

    def __init__(self, 
        content_type: str | None = None, 
        timestamp: str | None = None,
        dat: dict | None = None):

        if dat is not None:
            if not 'role' in dat:
                raise ValueError('Missing "role" field')
            self.role = dat['role']

            if not 'content' in dat:
                raise ValueError('Missing "content" field')

            if not 'content_type' in dat['content']:
                raise ValueError('Missing "content_type" in "content"')

        else:
            if timestamp is None:
                self._timestamp = datetime.now()
            else:
                self._timestamp = timestamp
            self._content_type = content_type

    @property 
    def content_type(self):
        """Provide context for the content"""
        return self._content_type

    @content_type.setter
    def content_type(self, value: str):
        print("setting content type: "+value )
        self._content_type = value

    @property
    def timestamp(self):
        """Set timestamp for message (default=now)"""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):

        # FIXME allow str or actual timestamp
        self._timestamp = value

class GenericContent(InsightfulMessageContent):
    def __init__(self,
        value,
        timestamp = None):

        super(StringContent, self).__init__('GENERIC', timestamp)
        self.value = value

    @property
    def value(self):
        return(self._value)

    @value.setter
    def value(self, value):
        self._value = value

class StringContent(InsightfulMessageContent):
    def __init__(self,
        value: str,
        timestamp = None):

        self.value = value

        super(StringContent, self).__init__('STRING', timestamp)

        self.value = value

    def __str__(self):
        """convert to loadable json"""
        out_str = f'"content_type": "STRING", "value": "{self.value}"'
        out_str = '{'+out_str+'}'
        return(out_str)

    @property
    def value(self):
        return(self._value)

    @value.setter
    def value(self, value: str):
        if not isinstance(value, type('')):
            raise ValueError("Input must be a string")
        self._value = value

    def from_json(self, json: dict):
        super(StringContent, self).from_json(json)

        if 'content_type' not in json['content']:
            raise ValueError('Missing "content_type" field')

        if json['content']['content_type'] != "STRING":
            raise ValueError('Wrong content_type StringContent: {json["content"]["content_type"]}')

        if 'value' not in json['content']:
            raise ValueError('Missing value')

        self.value = str(json['content']['value'])

class FileDirContent(InsightfulMessageContent):

    def __init__(self, 
        file: str | None = None, 
        file_list: list | None = None, 
        directory: str | None = None, 
        directory_list: list | None = None,
        timestamp = None):
 
        super(FileDirContent, self).__init__('FILEDIR', timestamp)

        bad_init = False
        if file is not None:
            if file_list is not None or directory is not None or directory_list is not None:
                bad_init = True
        if file_list is not None:
            if file is not None or directory is not None or directory_list is not None:
                bad_init = True  
        if directory is not None:
            if file is not None or file_list is not None or directory_list is not None:
                bad_init = True
        if directory_list is not None:
            if file is not None or file_list is not None or directory is not None:
                bad_init = True                

        if bad_init:
            raise ValueError("Can only set one of file, file_list, directory, directory_list")
        
        self._file = file

        self._file_list = file_list

        self._directory = directory

        self._directory_list = directory_list
    
    def __str__(self):
        """convert to json loadable string"""
        out_str = f'"content_type": "FILEDIR","timestamp":"{self.timestamp}"'
        if self.file is not None:
            out_str = out_str + f',"file":"{self.file}"'
        if self.directory is not None:
            out_str = out_str + f',"directory":"{self.directory}"'
        if self.file_list is not None:
            out_str = out_str + ',"file_list":['
            out_str = out_str + '"' + '","'.join(self.file_list) + '"'
            out_str = out_str + ']'
        if self.directory_list is not None:
            out_str = out_str + ',"directory_list":['
            out_str = out_str + '"' + '","'.join(self.directory_list) + '"'
            out_str = out_str + ']'
        out_str = '{'+out_str+'}'
        return(out_str)

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value: str):
        # don't check for valid file in case intent is file creation
        self._file = value

    @property
    def file_list(self):
        return(self._file_list)

    @file_list.setter
    def file_list(self, value: list[str]):
        self._file_list = value

    @property 
    def directory(self):
        return(self._directory)

    @directory.setter
    def directory(self, value: str):
        self._directory = value

    @property
    def directory_list(self):
        return(self._directory_list)

    @directory_list.setter
    def directory_list(self, value: list[str]):
        self._directory_list = value

def FileDirContentLoad(input: dict):
    fdc = FileDirContent(timestamp=input['timestamp'])
    if 'file' in input:
        fdc.file = input['file']

    return(fdc)


class InsightfulMessage:
    def __init__(self, 
        role: str | None = None, 
        content: str | dict = None):

        self._role=None
        self._content=None

        # base directory to start monitoring
        if role is not None:
            self.role = role

        if content is not None:
            self.content = content

    def __str__(self):
        content_str = str(self.content)
        out_str = f'{{"role":"{self.role}","content":{content_str}}}'
        #out_str = '{' + out_str + '}'
        return(out_str)

    @property 
    def role(self):
        return self._role

    @role.setter
    def role(self, value: str):
        if not value in ['user', 'system']:
            raise ValueError(f"Invalid role: {value}")
        self._role = value

    @property
    def content(self):
        return(self._content)

    @content.setter
    def content(self, value: str | dict):

        if isinstance(value, type('')):
            try:
                self._content = json.loads(value)
            except:
                self._content = str(value)
        else:
            self._content = value

def insightful_message_from_dict(dat: dict):

    msg = InsighfulMessageContent(json=json)

    if dat['content']['content_type']=="STRING":
        msg=StringContent.load_json(json)
