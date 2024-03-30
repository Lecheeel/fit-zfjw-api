# test_example.py

import JWGLClient  # 替换成您的模块名称

@pytest.fixture
def jwgl_client():
    account = ''
    password = ''
    base_url = 'http://oaa.fitedu.net/jwglxt'
    return JWGLClient(base_url, account, password)

def test_login(jwgl_client):
    main_page = jwgl_client.login()
    assert main_page.status_code == 200

def test_get_schedule(jwgl_client):
    schedule = jwgl_client.get_schedule()
    assert schedule.status_code == 200

def test_get_info(jwgl_client):
    info = jwgl_client.get_info()
    assert isinstance(info, dict)

if __name__ == "__main__":
    # 运行所有测试用例
    import pytest
    pytest.main([__file__])
