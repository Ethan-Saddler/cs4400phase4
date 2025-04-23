# CS4400 Phase 4

## Setup Instructions/Setup

1. Run database and procedures on my sqlworkbench

2. Set the password to your mysqlworkbench localhost (line 16 of app.py)

2. pip install -r requirements.txt

3. run `python app.py`

4. Go to `http://127.0.0.1:5001/`

## Technologies

1. Flask: this was used to create the backend server and handled the HTTP requests. Since it is written in python, it is trivial to connect to the MYSQL server using pymysql, which allowed us to call procedures with the parameters passed in from the frontend when a route was called. Another nice aspect of flask was that because it is based on routes, it made it much easier to compartmentalize and have different routes for each procedure.

2. HTML: this was used to make the core aspects and structure of the frontend and was the connection from the frontend to the flask backend.

3. CSS: this was used to do some basic styling on the frontend, so it was not super boring to look at.

## How Work was Distributed

We split the work by splitting up the individual procedures/views evenly. The nice thing about flask is that it is super easy to work simultaneously, as each route is independent of each other. So rather than using git, when each of us finished a procedure route, we put it in a google doc, then combined them all into one file when we finished. This also included the HTML, which was rather trivial as once we made the first iteration, we were able to basically copy that for the rest of the procedures. The styling in CSS was done by Ethan and Ben, since they were the most familiar with the syntax and conventions; however, this was the most trivial aspect of this implementation. Overall, we all put in an equal effort into finishing this and would not have been possibile without everyone's help.

