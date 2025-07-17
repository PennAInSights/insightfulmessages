import json
from datetime import datetime
from typing import Type

from insightfulmessages import InsightfulMessageContent
from insightfulmessages import FileDirContentLoad

class DicomEntity:
    """Basic connection info for a dicom entity"""

    def __init__(self, ae_title: str, addr: str, port: int | str | None):

        self._ae_title = ae_title
        self._addr = addr
        self._port = None

        if port is not None:
            self._port = int(port)

    def __str__(self):
        outstr = f'{{"ae_title":"{self.ae_title}","addr":"{self.addr}","port":{self.port}}}'
        return(outstr)

    @property
    def ae_title(self):
        return(self._ae_title)

    @ae_title.setter
    def ae_title(self, value: str):
        """Application Entity Title"""
        self._ae_title=value

    @property
    def addr(self):
        """IP address"""
        return(self._addr)

    @addr.setter
    def addr(self, value: str):
        self._addr = value

    @property
    def port(self):
        """TCP/IP port number"""
        return(self._port)

    @port.setter
    def port(self, value: int):
        if value < 0:
            raise ValueError(f'Invalid port {value}')
        self._port = port

def DicomEntityLoad(input: dict):
    dcm=DicomEntity(input['ae_title'],input['addr'],input['port'])
    return(dcm)

class DicomConnection:
    """Parameters used to establish a connection between dicom AEs as an SCU"""
    def __init__(self):
        self._dimse_timeout = None
        self._socket_timeout = None
        self._acse_timeout = None

    @property 
    def dimse_timeout(self):
        """timeout for DIMSE messages (in sec)"""
        return(self._dimse_timeout)

    @dimse_timeout.setter
    def dimse_timeout(self, value: int):
        if value < 0:
            raise ValueError(f'Invalid dimse_timeout {value}')
        self._dimse_timeout = value

    @property 
    def socket_timeout(self):
        """timeout for network socket (in sec)"""
        return(self._socket_timeout)

    @socket_timeout.setter
    def socket_timeout(self, value: int):
        if value < 0:
            raise ValueError(f'Invalid socket_timeout {value}')
        self._socket_timeout = value

    @property 
    def acse_timeout(self):
        """timeout for ACSE messages (in sec)"""
        return(self._acse_timeout)

    @acse_timeout.setter
    def acse_timeout(self, value: int):
        if value < 0:
            raise ValueError(f'Invalid acse_timeout {value}')
        self._acse_timeout = value

    def __str__(self):
        outstr = f'{{"dimse_timeout":"{self.dimse_timeout}","socket_timeout":"{self._socket_timeout}","acse_timeout":"{self.acse_timeout}"}}'
        return(outstr)

def DicomConnectionLoad(input: dict):
    dcm=DicomConnection()
    if input['socket_timeout'] != "None":
        dcm.socket_timeout = int(input['socket_timeout'])
    if input['acse_timeout'] != "None":
        dcm.acse_timeout = int(input['acse_timeout'])
    if input['dimse_timeout'] != "None":
        dcm.dimse_timeout = int(input['dimse_timeout'])
    return(dcm) 

class DicomContent(InsightfulMessageContent):

    def __init__(self, timestamp=None):

        super(DicomContent, self).__init__('DCM', timestamp)

        # Sting indicating the request type (e.g. "C-STORE")
        self._operation = None

        # DicomEntity with details about the sending AE
        self._sender = None

        # DicomEntity with detail about the receiving AE
        self._receiver = None

        # Parameters specific to the requested operation
        self._op_parameters = None

        # Parameters for AE-to-AE connection
        self._connection = DicomConnection()

    def __str__(self):
        """Print string suitable for json loading"""
        out_str = f'{{"content_type":"{self.content_type}","timestamp":"{self.timestamp}",'
        out_str += f'"operation":"{self.operation}",'
        conn_str = str(self.connection)
        out_str += f'"connection": {conn_str},'
        sender_str = str(self.sender)
        out_str += f'"sender": {sender_str},'
        receiver_str = str(self.receiver)
        out_str += f'"receiver": {receiver_str},'
        op_param_str = str(self.op_parameters)
        out_str += f'"op_parameters":{op_param_str}}}'

        return(out_str)

        
    @property
    def operation(self):
        """Type of request"""
        return self._operation

    @operation.setter
    def operation(self, value: str):
        if not value in ['C-STORE', 'C-FIND']:
            raise ValueError(f'Unsupported operation: {value}')
        self._operation = value

    @property
    def sender(self):
        """Info about sending AE"""
        return self._sender

    @sender.setter
    def sender(self, value: DicomEntity):
        self._sender = value
        
    @property
    def receiver(self):
        """Info about receiving AE"""
        return self._receiver

    @receiver.setter
    def receiver(self, value: DicomEntity):
        self._receiver = value

    @property
    def connection(self):
        """Parameters for AE-to-AE connection"""
        return(self._connection)

    @connection.setter
    def connection(self, value: DicomConnection):
        self._connection = value

    @property
    def op_parameters(self):
        """Parameters for the request operation type"""
        return(self._op_parameters)

    @op_parameters.setter
    def op_parameters(self, value):
        self._op_parameters = value

def DicomContentLoad(content: dict | str):
    """Load content from a dict or str"""
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except json.decoder.JSONDecodeError:
            print("Could not read json")
            return(None)

    # Content common to all dicom requests
    dcm = DicomContent(content['timestamp'])
    dcm.operation = content['operation']
    dcm.sender = DicomEntityLoad(content['sender'])
    dcm.receiver = DicomEntityLoad(content['receiver'])
    dcm.connection = DicomConnectionLoad(content['connection'])

    # Content specific to operation
    if dcm.operation=="C-STORE":
        dcm.op_parameters = FileDirContentLoad(content['op_parameters'])

    return dcm


