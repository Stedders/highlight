from app.helpers import set_gravatar


def test_set_gravatar():
    gravatar = set_gravatar('spam@eggs.py', 'assets/media/avatar.jpg', 25)
    assert gravatar == 'https://www.gravatar.com/avatar/d727572192d346449867d2bc20f1d3f3?d=assets%2Fmedia%2Favatar.jpg&s=25'