from models import User, CaseSummary, ChatFile, Collection

def test(client):
    # Get a reference to the 'sample_mflix' database:
    db = client['lawyerly']

    # Create test user
    User('gary.smith@gmail.com', 'Gary', 'Smith')
    User('gary.smith@gmail.com').save()
