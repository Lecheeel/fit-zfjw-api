import pytest
from main import JWGLClient  # 替换成您的模块名称

@pytest.fixture
def jwgl_client():
    account = '2301123104'
    password = 'Ryancuee85173'
    base_url = 'http://oaa.fitedu.net/jwglxt'
    return JWGLClient(base_url, account, password)

def test_login(jwgl_client):
    main_page = jwgl_client.login()
    assert main_page.status_code == 200

def test_get_schedule(jwgl_client):
    schedule = jwgl_client.get_schedule()
    assert schedule.status_code == 200
    assert 'courseList' in schedule.json()  # 检查返回的 JSON 数据中是否包含课程列表

def test_get_info(jwgl_client):
    info = jwgl_client.get_info()
    assert isinstance(info, dict)
    assert 'name' in info  # 检查返回的个人信息中是否包含姓名字段
    assert 'studentId' in info  # 检查返回的个人信息中是否包含学号字段

def test_invalid_login():
    account = ''
    password = ''
    base_url = 'http://oaa.fitedu.net/jwglxt'
    client = JWGLClient(base_url, account, password)
    with pytest.raises(Exception):
        client.login()

if __name__ == "__main__":
    pytest.main([__file__])
