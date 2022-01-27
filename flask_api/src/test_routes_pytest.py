from services.app import app_test


def test_home():
    # Test the route to the main page.
    response = app_test.test_client().get('/')

    assert response.status_code == 200
    assert response.status_code != 404


def test_home_no_succes():
    # Test the route to a wrong url to main page.
    response = app_test.test_client().get('/.')

    assert response.status_code == 404
    assert response.status_code != 200


def test_login():
    # Test the route to the login wrong page.
    response = app_test.test_client().get('/loginn')

    assert response.status_code == 404
    assert response.status_code != 200
