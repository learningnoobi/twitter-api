# twitter-api
Django Rest framework Real Time Twitter API . Fully functional twitter app with websocket api to notify and send chat in real time using django channels.

FrontEnd is in React js . 

React Code : https://github.com/learningnoobi/twitter-react
## how to run
`mkdir yourfolder` </br>
`cd yourfolder` </br>
`virtualenv env`</br> 
`source env/bin/activate`</br>
`git clone https://github.com/learningnoobi/twitter-api.git` </br>
`pip install -r requirements.txt`</br>
`cd twitter-api`</br>
`python manage.py runserver`</br>
Note: private info are added in .env file so create new .env file in root add them there
### .env file looks like this

`SECRET_KEY=yoursecretkey`</br>
`email=youremail`</br>
`password=yourapppassword`</br>
`cloud_name=cloudinaryname`</br>
`api_key=cloudinaryapikey`</br>
`api_secret=cloudinarysecretkey`</br>
