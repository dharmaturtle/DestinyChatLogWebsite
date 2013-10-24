# [Destiny Chat Log Website](http://ec2-54-241-15-193.us-west-1.compute.amazonaws.com:8080/)
## Now in Django and MongoDB!

I decided to learn my favourite language's most popular web framework, NoSQL, and map reduce, since my past web experience has been with Ruby on Rails and MySQL.

[![websitescreenshot](https://raw.github.com/dharmaturtle/DestinyChatLogWebsite/master/screenshot.PNG)](http://ec2-54-241-15-193.us-west-1.compute.amazonaws.com:8080/)

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

There are a ton of features I want to implement. The screenshot will become quickly outdated. Visit the site [here](http://ec2-54-241-15-193.us-west-1.compute.amazonaws.com:8080/)!

In the works:

* Hyperlinked timestamps
* Timezone detection and customization views/searches with JavaScript
* More statistics (more map reduce!)
* Convert floats to ints in Statistics
* Many, many small bug fixes

Code will be uploaded when I'm done ironing out bugs. Map reduce scripts are available, though.