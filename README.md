# Destiny Chat Log Website
## Now in Django and MongoDB - [See it live here!](http://ec2-54-241-15-193.us-west-1.compute.amazonaws.com:8080/)

I decided to learn my favourite language's most popular web framework and NoSQL, since my past web experience has been with Ruby on Rails and MySQL.

![websitescreenshot](https://raw.github.com/dharmaturtle/DestinyChatLogWebsite/master/screenshot.png)

## How to use

`pip freeze` says I'm using these:

    Django==1.3.7
    argparse==1.2.1
    distribute==0.6.24
    django-mongodb-engine==0.4.0
    djangotoolbox==0.9.2
    pymongo==2.6.3
    wsgiref==0.1.2

I'm using the `nonrel` fork of Django. Follow the guide [here](http://django-mongodb-engine.readthedocs.org/en/latest/topics/setup.html), but be prepared to Google some error messages. If you run into `Please make sure your SITE_ID contains a valid ObjectId string.`, [StackOverflow](http://stackoverflow.com/questions/8819456/django-mongodb-engine-error-when-running-tellsiteid/19509204#19509204) has many solutions.

## To do

There are a ton of features I want to implement. The screenshot will become quickly outdated, just visit the site [here](http://ec2-54-241-15-193.us-west-1.compute.amazonaws.com:8080/)!