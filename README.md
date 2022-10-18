# Be Your Own Zookeeper

Learn more about the developer: [Michaela Healton's LinkedIn](https://www.linkedin.com/in/michaela-healton/)

Be Your Own Zookeeper is a fullstack web application that allows users to:

- Check if their local weather is good for taking a walk
- Set a daily schedule wiht optional text reminders for self care tasks
- Consult a checklist of common reasons for feeling bad and recieve gentle advice for how to resolve those problems

![Be Your Own Zookeeper Homepage](/static/img/be-your-own-zookeeper-homepage.png)

## Features

Be You Own Zookeeper was named for a quote from tumblr user soaringsearingphoenix ["The worst part of human adulthood is being your own zookeeper"](https://soaringsearingphoenix.tumblr.com/post/634871709833560064/like-i-have-to-make-sure-my-meals-are). It is in the spirit of this quote that Be Your Own Zookeeper aims to make self care a little simpler. 

The first way that Be Your Own Zookeeper does this is by allowing users to automate deciding whether or not the weather is good enough to take a walk. By setting weather preferences, users can make it so that the first thing they see when they log in is an answer to the question: Is the weather good for walking? Users can also customize a list of alternate activities to do when the weather isn't good for walking, once again cutting down on the amount of thinking required to get moving and do a physical activity. 

![Be Your Own Zookeeper Logged In Homepage](/static/img/logged-in-homepage.png)

Another important feature of Be Your Own Zookeeper is the daily schedule. This schedule allows users to set up a daily list of reminders that will be optionally texted to them at specific times. Moreover, if users want to take a walk, they can set the type of the reminder to indicate that, and at the time the reminder is sent that user's local weather will be checked against their customized weather preferences and the reminder that is sent will either send the user the personalized reminder text that they've set or a message declaring that the weather is not good for walking and offering a random one of the user's alternate activities as a suggestion. 

![Be Your Own Zookeeper Schedule Page](/static/img/schedule.png)

Finally, there is the Be Your Own Zookeeper Checklist For When Everything Feels Bad. This customizable checklist helps users check in with their physical, social, and emotional needs. It can have items added to it, removed from it, and reorganized within it totally at the discretion of the user. 

![Be Your Own Zookeeper Checklist Page](/static/img/checklist.png)

## Technologies Used

- Python 
- HTML 
- CSS 
- JavaScript (AJAX, JSON)
- Cron 
- PostgreSQL
- SQLAlchemy
- Flask
- Jinja
- Bootstrap
- passlib.hash 
- uuid
- datetime
- flask_crontab

## Author
Michaela Healton is a software engineer in San Francisco, CA. 