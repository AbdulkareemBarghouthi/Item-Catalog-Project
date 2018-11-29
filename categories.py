from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Database import Categories, CategoryItem, Base, subCategories

engine = create_engine('sqlite:///categorymenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# # items for visuals
category1 = Categories(name="Visuals", description="""This
                      section provides categories
                      of visual entertainment!.""")
session.add(category1)
session.commit()

subcategory1 = subCategories(name="Movies", category=category1)
session.add(subcategory1)
session.commit()

subcategory2 = subCategories(name="Series", category=category1)
session.add(subcategory2)
session.commit()

subcategory3 = subCategories(name="Short films", category=category1)
session.add(subcategory3)
session.commit()

subcategory4 = subCategories(name="Paintings", category=category1)
session.add(subcategory4)
session.commit()

subcategory5 = subCategories(name="Photography", category=category1)
session.add(subcategory5)
session.commit()

subcategory6 = subCategories(name="Animation", category=category1)
session.add(subcategory6)
session.commit()

# Items for Audio section

category1 = Categories(name="Audio", description="""This section provides
                       audio entertainment,
                       if you're a music geek
                       or just someone who likes to listen
                       to podcasts then this site is for you!""")
session.add(category1)
session.commit()
subcategory1 = subCategories(name="Music", category=category1)
session.add(subcategory1)
session.commit()

subcategory2 = subCategories(name="Podcasts", category=category1)
session.add(subcategory2)
session.commit()

subcategory3 = subCategories(name="Audio Books", category=category1)
session.add(subcategory3)
session.commit()

# Itemss for gaming section
category1 = Categories(name="Gaming",
                       description="""Whether it's call of
                       duty or candy
                       crush you can store your favorite games here!""")

session.add(category1)
session.commit()
subcategory1 = subCategories(name="Console", category=category1)

session.add(subcategory1)
session.commit()

subcategory2 = subCategories(name="PC", category=category1)

session.add(subcategory2)
session.commit()

subcategory3 = subCategories(name="Other", category=category1)

session.add(subcategory3)
session.commit()

# Items for reading section
category1 = Categories(name="Reading",
                       description="""Hello book worms get ready to
                       store your favorite books here!""")

session.add(category1)
session.commit()
subcategory1 = subCategories(name="Books", category=category1)

session.add(subcategory1)
session.commit()

subcategory2 = subCategories(name="Articles", category=category1)

session.add(subcategory2)
session.commit()

subcategory3 = subCategories(name="Research", category=category1)

session.add(subcategory3)
session.commit()

# Items for random section!
category1 = Categories(name="Random",
                       description="""If you have random or other
                       things you can add them here""")

session.add(category1)
session.commit()
subcategory1 = subCategories(name="Random", category=category1)
session.add(subcategory1)
session.commit()
