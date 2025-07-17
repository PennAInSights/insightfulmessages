import pytest
import insightfulmessages as im

def test_dicom_message():

    d = im.DicomContent()
    assert d.content_type == "DCM"

    d.operation="C-STORE"
    d.sender = im.DicomEntity('SCU','localhost',0)
    d.receiver = im.DicomEntity('SCP','localhost',4242)
    d.op_parameters = im.FileDirContent(file="/path/to/filename.dcm")
    msg = im.InsightfulMessage('user', d)
    new_msg = im.insightful_message_load(str(msg))

    assert str(msg) == str(new_msg)

if __name__ == "__main__":
    pytest.main()