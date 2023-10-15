# ProAssist
Deployed Live API Documentation here: https://proassist.up.railway.app/docs/

ProAssist consists of a REST API with dynamic features for webapps focused on bridging the gap between skilled professionals and clients. It offers features such as creation of job openings for professionals, allocation of those jobs to a qualified professional, obtaining free professionals with no jobs at hand, review and rating of professionals and many more. It also has a dedicated real time one to one communication chat server between clients and professionals by implementing the power of WebSockets.

Job openings created by clients in proassist are divided into three: 'NA' for Non-Allocated(jobs with no assigned professional), 'P' for Pending(jobs still attended to by a professional), 'C' for Completed(jobs completed by a professional).

Below is the list of all professions by professionals in ProAssist:
- Cleaner
- Plumber
- Barber
- Gardener
- HairStylist
- Cook
- Nanny
- GarbageCollector
- Painter
- Electrician
- Carpenter
- Mechanic

# Features
API

- Non-Allocated jobs are displayed according to each professional's profession on their respective home page.
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

# Installation and Usage
1. Clone the repository

``` $ git clone https://github.com/AyobomiOmojola/ProAssist.git ```

3. Comment out the production PostgreSQL database in the settings file and replace with SQLlite for use in development
4. Repeat the above step also for redis and have a redis docker container running on your local machine
5. Create and activate a virtual environment for this project

``` $ python -m venv venv ```
``` $ source venv/bin/activate ```

6. Install project dependencies

``` $ pip install -r requirements.txt ```

8. Run database migrations
   
``` $ py manage.py migrate ```

10. Create superuser to access the admin dashboard
    
``` $ py manage.py createsuperuser ```

12. Run the development server
    
``` $ py manage.py runserver ```

13. Access the application at http://127.0.0.1:8000

# Authors
ProAssist is developed and maintained by Ayo Omojola




