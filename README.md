# insightfulmessages
Helper classes to created structured message for use with RabbitMQ


## Features

## Installation

You can install the package via  **source**


### Install from Source (github)

```bash
git clone https://github.com/PennAInSights/insightfulmessages.git
cd insightfulmessages
pip install .
```


## Usage 
After installation you can create an 'InsightfulMessage' to send to another app

### Basic Example

```python
import insightfulmessages as im

msg_content = im.StringContent("Hello messaging world!")
msg = im.InsightfulMessage('user', msg_content)

# Show what is in the message
print(msg.role)
print(msg.content)

# Convert to string that is loadable as json
msg_string = str(msg)
print(mst_string)
```

### Build message to request a dicom c-store operation
```python
import insightfulmessages as im

# Request transfer of file/s to a PACS
rq = im.DicomContent()
rq.operation = "C-STORE"
rq.op_parameters = im.FileDirContent(file='/path/to/my_instance.dcm')

# scu = service class users = who is sending the request
rq.sender = im.DicomEntity('DCMSCU', 'localhost', None)

# scp = service class provider = who is receiving the request
rq.receiver = im.DicomEntity('DCMSCP', 'localhost', 4242)

# construct final message
msg = im.InsightfulMessage('user', rq)

# create a json parseable string
msg_str = str(msg)

```

msg_str now contains the following json data

```json
{
"role":"user",
"content": {
    "content_type":"DCM",
    "timestamp":"2025-07-15 16:55:02.856232",
    "operation":"C-STORE",
    "op_parameters":{
        "content_type": "FILEDIR",
        "timestamp":"2025-07-15 17:56:56.757643",
        "file":"/path/to/file.dcm"
        },
    "connection": {
        "dimse_timeout":"None",
        "socket_timeout":60,
        "acse_timeout":30
        },
    "sender": {
        "ae_title":"SCU",
        "addr":"localhost",
        "port":0
        },
    "receiver": {
        "ae_title":"SCP",
        "addr":"localhost",
        "port":4242
        }
    }
}
```
