import requests

def test_upload():
    url = 'http://127.0.0.1:5003/upload'
    file_path = 'uploads/20016.dcm'
    
    with open(file_path, 'rb') as f:
        files = {'file': ('20016.dcm', f, 'application/dicom')}
        response = requests.post(url, files=files)
    
    print('Response status:', response.status_code)
    print('Response content:', response.text)

if __name__ == '__main__':
    test_upload() 