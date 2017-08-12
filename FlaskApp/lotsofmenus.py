from database import db_session, User,  MenuItem, Restaurant, RestaurantAddress


# Create fake user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
db_session.add(User1)
db_session.commit()

# Menu for UrbanBurger
restaurant1 = Restaurant(user_id=1, name="Urban Burger", phone="1111112222", email="test@test.com", food_type="mix",
                         website="www.test.com", description="test")

db_session.add(restaurant1)
db_session.commit()

restaurantaddres = RestaurantAddress(restaurant_id=1, street="1 road", city="lansing",
                                     state="Michigan", zip_code="48910")

db_session.add(restaurantaddres)
db_session.commit()

menuItem2 = MenuItem(user_id=1, name="Veggie Burger",
                     description="Juicy grilled veggie patty with tomato mayo and lettuce", price="$7.50",
                     course="Entree", restaurant=restaurant1)

db_session.add(menuItem2)
db_session.commit()

menuItem1 = MenuItem(user_id=1, name="French Fries", description="with garlic and parmesan", price="$2.99",
                     course="Appetizer", restaurant=restaurant1)

db_session.add(menuItem1)
db_session.commit()

menuItem2 = MenuItem(user_id=1, name="Chicken Burger",
                     description="Juicy grilled chicken patty with tomato mayo and lettuce", price="$5.50",
                     course="Entree", restaurant=restaurant1)

db_session.add(menuItem2)
db_session.commit()

menuItem3 = MenuItem(user_id=1, name="Chocolate Cake", description="fresh baked and served with ice cream",
                     price="$3.99", course="Dessert", restaurant=restaurant1)

db_session.add(menuItem3)
db_session.commit()

menuItem4 = MenuItem(user_id=1, name="Sirloin Burger", description="Made with grade A beef", price="$7.99",
                     course="Entree", restaurant=restaurant1)

db_session.add(menuItem4)
db_session.commit()

menuItem5 = MenuItem(user_id=1, name="Root Beer", description="16oz of refreshing goodness", price="$1.99",
                     course="Beverage", restaurant=restaurant1)

db_session.add(menuItem5)
db_session.commit()

menuItem6 = MenuItem(user_id=1, name="Iced Tea", description="with Lemon", price="$.99", course="Beverage",
                     restaurant=restaurant1)

db_session.add(menuItem6)
db_session.commit()

menuItem7 = MenuItem(user_id=1, name="Grilled Cheese Sandwich", description="On texas toast with American Cheese",
                     price="$3.49", course="Entree", restaurant=restaurant1)

db_session.add(menuItem7)
db_session.commit()

menuItem8 = MenuItem(user_id=1, name="Veggie Burger",
                     description="Made with freshest of ingredients and home grown spices", price="$5.99",
                     course="Entree", restaurant=restaurant1)

db_session.add(menuItem8)
db_session.commit()

print ("added menu items!")
