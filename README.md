# ProAssist
Deployed Live API Documentation here: https://proassist.up.railway.app/docs/

ProAssist consists of a REST API with dynamic features for webapps focused on bridging the gap between skilled professionals and clients. It offers features such as creation of job openings for professionals, allocation of those jobs to a qualified professional, obtaining free professionals with no jobs at hand, review and rating of professionals and many more. It also has a dedicated real time one to one communication chat server between clients and professionals by implementing the power of WebSockets.

Job openings created by clients in proassist are divided into three: 'NA' for Non-Allocated (jobs with no assigned professional), 'P' for Pending (jobs still attended to by a professional), 'C' for Completed (jobs completed by a professional).

Below is the list of all professions by professionals in ProAssist:
- Cleaner
- Plumber
- Barber
- Gardener
- Hair-Stylist
- Cook
- Nanny
- Garbage-Collector
- Painter
- Electrician
- Carpenter
- Mechanic

# Features
API

- Non-Allocated jobs are displayed according to each professional's profession on their respective home page
- Creation of job openings for professionals by clients
- Assigning of jobs to qualified professionals
- Obtaining all Non-Allocated job openings by professionals
- Obtaining free professionals with no jobs at hand (by profession)
- Set a job as completed after a professional as rendered the needed service of such job
- Rating and Review of professionals
- Signing-up, Signing-in and logging-out of users
- Creation and Updating of Userprofiles
- Display of Userprofiles with respective ratings, reviews, pending and completed jobs

CHAT SERVER

ProAssist offers a chat feature to enable clients to chat with professionals whose services they need rendered. Below is an example of this; jane who is a client is chatting with a professional named john who is an electrician.

![Screenshot (351)](https://github.com/AyobomiOmojola/ProAssist/assets/145074091/1d292cd5-aba9-42b6-97f3-f23089b328e9)

![Screenshot (352)](https://github.com/AyobomiOmojola/ProAssist/assets/145074091/ac279652-66e9-4ea9-a97c-f52f26b3a7e8)

Below are links in order to test the live chat server; Two users with non expiry tokens have been registered:
Both chat screens can be loaded on say two different browsertabs.

To chat as Jane: https://proassist.up.railway.app/chat/john/?token=c5c0f6d7f4df1ae188eb2344bb96911a432b7402

To chat as John: https://proassist.up.railway.app/chat/jane/?token=b16facf56bb7564389d7db4e09dcf93bc14b94f8


# Installation and Usage
1. Clone the repository

``` $ git clone https://github.com/AyobomiOmojola/ProAssist.git ```

2. Comment out the production PostgreSQL database in the settings file and replace with SQLlite for use in development
   
3. Repeat the above step also for redis and have a redis docker container running on your local machine
   
4. Create and activate a virtual environment for this project

``` $ python -m venv venv ```

``` $ source venv/bin/activate ```

5. Install project dependencies

``` $ pip install -r requirements.txt ```

6. Run database migrations
   
``` $ py manage.py migrate ```

7. Create superuser to access the admin dashboard
    
``` $ py manage.py createsuperuser ```

8. Run the development server
    
``` $ py manage.py runserver ```

9. Access the live API documentation at ```http://127.0.0.1:8000/docs```
    
10. Where USERNAME = Username of the user you want to chat with and TOKEN = Your Login Token;
    
Hence access the chat server at ```http://127.0.0.1:8000/USERNAME/?token=TOKEN```

(You could register and login users and follow the url guide above to correctly load their chat screens on say two different browser tabs)

# Authors
ProAssist is developed and maintained by Ayo Omojola




