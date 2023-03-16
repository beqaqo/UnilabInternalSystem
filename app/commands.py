from flask.cli import with_appcontext
from app.extensions import db
from app.models.user import User, Country, Region, City, University
from app.models.roles import Role, UserRole
from app.models.subjects import Subject, ActivityType, Announcement, AnnouncementUser
import click



@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Creating Database")
    db.drop_all()
    db.create_all()
    click.echo("Finished Creating Database")


@click.command("populate_db")
@with_appcontext
def populate_db():
    click.echo("populating db")

    #populating country table
    countries = ["საქართველო", "საფრანგეთი", "გერმანია", "ავსტრია", "დიდი ბრიტანეთი"]
    for country in countries:
        country_ = Country(country_name = country)
        country_.create()
    country_.save()

    #populating region table
    regions = ["იმერეთი", "სვანეთი", "გურია", "რაჭა", "კახეთი"]
    for region in regions:
        region_ = Region(region_name = region)
        region_.create()
    region_.save()

    #populating city table
    cities = ["ქუთაისი", "თბილისი", "ზუგდიდი", "ბათუმი", "გორი"]
    for city in cities:
        city_ = City(city_name = city)
        city_.create()
    city_.save()

    #populating university table
    unisversities = ["ილიაუნი", "თსუ", "თსსუ", "გტუ", "სამხატვრო"]
    for university in unisversities:
        university_ = University(university_name = university)
        university_.create()
    university_.save()

    #populating roles table 
    roles = ["ადმინი", "სტუდენტი", "ლექტორი", "მოდერატორი"]
    for role in roles:
        role_ = Role(name = role)
        role_.create()
    role_.save()

    #populating subjects 
    subjects = ["პითონი", "HTML/CSS", "ჯავასკრიპტი", "C++"]
    for subject in subjects:
        subject_ = Subject(name = subject)
        subject_.create()
    subject_.save()

    type = ActivityType(name = "კურსი")
    type.create() 
    type = ActivityType(name = "სტაჟირება")
    type.create() 
    type.save()


    click.echo("done populating")