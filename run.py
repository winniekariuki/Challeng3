

from app import create_app
from app.api.v2.models import *

data = {"username":"Winnie","email":"winniekariuki07@gmail.com","password":"winnie07@","role":"Admin"}
admin = User(data)
admin.save_admin() 

app = create_app("development")

if __name__ == "__main__":
	app.run(debug=True) 


