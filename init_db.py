
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db
from models import User , Product, Delivery


db.create_all()

admin_user = User(
    username='admin',
    password= "password",
    is_admin=True
)

db.session.add(admin_user)
db.session.commit()

products = [
    Product(name='Harry Potter Wands', price = 14.99, description="The magic wand used in the Harry Potter movies is a very good and necessary accessory for Harry Potter fans." , image_url="wand.jpg", rating=0.0),
    Product(name='Dc.Strange Magic Box', price=11.99,description = "A magic box for fans of Doctor Strange, including the ultimate magic accessories, posters and necklace."  , image_url="dc_strange_2.jpg", rating=0.0),
    Product(name='Snitch From Harry Potter', price=7.99,description ="Legendary, Fast, Beautiful Snitch From Harry Potter Movies, Which will help you understand the world of Harry Potter better"  , image_url="snitch.jpg", rating=0.0),
    Product(name='DC.Strange Magic Box', price=11.99,description=" magic box for fans of Doctor Strange, including the ultimate magic accessories, posters and necklace.",image_url="dc_strange_2.jpg", rating=0.0),
    Product(name='One Piece Box', price=12.99,description = "Experience the extraordinary abilities of the One Piece characters with special effects and features that can be activated." , image_url="onepiece.png", rating=0.0),
    Product(name='Lord Of The Rings Box', price=12.99,description="Discover and collect legendary items from the Lord of the Rings universe, each with its own history and magical properties.",image_url="lord_of_the_rings_box.png", rating=0.0),
    Product(name='Demon Slayer VOL1', price=8.99,description ="Experience the magic and power of the demon slayers with special effects and abilities that can be activated."  , image_url="demon_slayer.png", rating=0.0),
    Product(name='One Piece Box', price=12.99, description ="Experience the extraordinary abilities of the One Piece characters with special effects and features."  ,image_url="onepiece.png", rating=0.0,)

    ]


db.session.bulk_save_objects(products)
db.session.commit()



