# AskMate (sprint 2)

## Story
 
Last week you created a pretty good site from scratch. It already has some features but it's a bit difficult to maintain due to the fact that we store data in csv files and we also need some more features to make it more usable and more appealing to users.

The management decided to move further as users requested new features like ability to comment on answers and tag questions (and here is the issue with csv files as well). There are several other feature requests which you can find in the user stories.

The management decided to put more ownership on the development team so now there is no compulsory stories. Of course the best case according to them if all of the stories are implemented but now it's more important that you, **the development team should choose the stories in order to maximize business values for the sprint**. So first, choose the stories and after that ask a mentor to validate it.

The management was very interested in the agile development methodologies that they just recently hear about, thus they are handing out a **prioritized list** of user stories called a product backlog. Try to estimate how many of these stories your team can finish until the demo. As the order is important, you should choose from the beginning of the list as much as you can, **the first four stories are the most important**.


## What are you going to learn?

- how to use `psycopg2` to connect to a PostgreSQL database from Python,
- SQL basic commands (SELECT, UPDATE, DELETE, INSERT)
- CSS basics
- how to work according to the `Scrum` framework,
- how to create a `sprint plan`,


## Tasks


1. Make the application use a database instead of CSV files.

    - The application uses a PostgreSQL database instead of CSV files
    - The application respects the `PSQL_USER_NAME`, `PSQL_PASSWORD`, `PSQL_HOST` and `PSQL_DB_NAME` environment variables
    - The database structure (tables) is the same as in the provided SQL file (`sample_data/askmatepart2-sample-data.sql`)

2. Allow the user to add comments to a question.

    - There is a `/question/<question_id>/new-comment` page
    - The page is linked from the question's page
    - There is a form with `message` field, and issues `POST` requests
    - After submitting, you are redirected back to the question detail page, and the new comment appears together with submission time

3. Allow the user to add comments to an answer.

    - There is a `/answer/<answer_id>/new-comment` page
    - The page is linked from the question's page, next to or below the answer
    - There is a form with `message` field, and issues `POST` requests
    - After submitting, you are redirected back to the question detail page, and the new comment appears together with submission time

4. Implement searching in questions and answers. (Hint: [Passing data from browser](https://learn.code.cool/web-python/#/../pages/web/passing-data-from-browser))


    - There is a search box and "Search" button on the main page
    - When you write something and press the button, you see a results list of questions (same data as in the list page)
    - The results list contains questions for which the title or description contain the searched phrase
    - The results list also contains questions which have answers for which the message contains the searched phrase
    - The results list has the following URL: `/search?q=<search phrase>`

5. Allow the user to edit the posted answers.

    - There is a `/answer/<answer_id>/edit` page
    - The page is linked from the answer's page
    - There is a form with a `message` field, and issues a `POST` request
    - The field is pre-filled with existing answer's data
    - After submitting, you are redirected back to the question detail page, and the answer is updated

6. Allow the user to edit comments.

    - The page URL is `/comment/<comment_id>/edit`
    - There is a link to the edit page next to each comment
    - The page contains a `POST` form with a `message` field
    - The field pre-filled with current comment message
    - After submitting, you are redirected back to question detail page, and the new comment appears
    - The submission time is updated
    - There is a message that says "Edited `<number_of_editions>` times." next to or below the comment

7. Allow the user to delete comments.

    - There is a recycle bin icon next to the comment
    - Clicking the icon asks the user to confirm the deletion
    - The deletion itself is implemented by the `/comments/<comment_id>/delete` endpoint (which does not ask for confirmation anymore)
    - After deleting, you are redirected back to question detail page, and the comment is not showed anymore

8. Display latest 5 questions on the main page (`/`).

    - The main page (`/`) displays the latest 5 submitted questions
    - The main page contains a link to all of the questions (`/list`)

9. Implement sorting for the question list. [If you did this user story in the previous sprint, now you only have to rewrite it to use SQL]

    - The question list can be sorted by title, submission time, message, number of views, and number of votes
    - You can choose the direction: ascending or descending
    - The order is passed as query string parameters, for example `/list?order_by=title&order_direction=desc`

10. Add tags to questions.

    - The tags are displayed on the question detail page
    - There is an "add tag" link which leads to the page for adding a tag
    - The page for adding a tag has the URL `/question/<question_id>/new-tag`
    - The page allows to either choose from existing tags, or define a new one.

11. Highlight the search phrase in the search results.

    - On the search results page, the searched phrase should be highlighted
    - If the phrase is found in an answer, the answer is also displayed (slightly indented)
    - The search phrase is also highlighted in the answers

12. Allow the user to delete tags from questions

    - There is an X link next to each tag
    - Clicking that link deletes the tag and reloads the question page
    - The deletion is implemented as `/question/<question_id>/tag/<tag_id>/delete` endpoint


## General requirements


None

## Hints

  * It's important that if the database table has a timestamp column then you cannot insert a UNIX timestamp value directly into that table, you should use:
    * either strings in the following format '1999-01-08 04&colon;05&colon;06',
    * or if you use psycopg2 and the datetime module, you can pass a datetime object to the SQL query as parameter (details in the background materials: [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation))
  * Pay attention on the order of inserting data into the tables, because you may violate foreign key constraints (that means e.g. if you insert data into the question_tag before you insert into the tag table the corresponding tag id you want to refer to then it won't exist yet)!
  * You can import the sample data file into `psql` with the `\i` command or run it via the Database tool in PyCharm.
  * Some user stories may require to deal with CSS as well, but do not deal with CSS too much. It's more important that you write proper queries, have a working connection with psycopg2, have a clean Python code than create an amazingly beautiful web application (although if you have time, of course it's not forbidden to do so :smiley:).


### Data models

All data should be persisted in a PostgreSQL database in the following tables (you can ignore data in the not implemented fields):

![AskMate data model part 2](../../media/web-python/askmate-data-model-part-2.png)

**question table**<br>
*id:* A unique identifier for the question<br>
*submission_time:* The date and time when the question was posted<br>
*view_number:* How many times this question was displayed in the single question view<br>
*vote_number:* The sum of votes this question has received<br>
*title:* The title of the question<br>
*message:* The question text<br>
*image:* the path to the image for this question<br>

**answer table**<br>
*id:* A unique identifier for the answer<br>
*submission_time:* The date and time when the answer was posted<br>
*vote_number:* The sum of votes this answer has received<br>
*question_id:* The id of the question this answer belongs to<br>
*message:* The answer text<br>
*image:* The path to the image for this answer<br>

**tag table**<br>
*id:* A unique identifier for the tag<br>
*name:* The name of the tag<br>

**question_tag table**<br>
*question\_id:* The id of the question the tag belongs to<br>
*tag\_id:* The id of the tag belongs to the question<br>

**comment table**<br>
*id:* A unique identifier for the comment<br>
*question\_id:* The id of the question this comment belongs to (if the comment belongs to an answer, the value of this field should be NULL)<br>
*answer\_id:* The id of the answer this comment belongs to (if the comment belongs to a question, the value of this field should be NULL)<br>
*message:* The comment text<br>
*submission\_time:* The date and time the comment was posted or updated<br>
*edited\_number::* How many times this comment was edited<br>

### Database and sample data

To init the database you've got a new SQL file in this repository on the `sprint-2` branch. As you'll learn about git branching later, here is a quick guide on how to merge the `sprint-2` branch to your `master` branch:

  * Go to your projects git repo folder you used last week
  * Tag the current commit so we can clearly see the end of the first sprint later<br>
   `git tag sprint-1-finished`
  * Merge the `sprint-2` branch of the repo into the master branch:<br>
   `git merge -X theirs origin/sprint-2 -m 'Merge sprint-2 branch'`
  * As there is a new README.md there will be a merge conflict, but with the command above it will be resolved automatically. The `sprint-2` branch version of the README.md will overwrite the old one.
  * Now you have the `sample_data/askmatepart2-sample-data.sql` file in your repository.


## Starting repository

> **For your information**: Unfortunately, GitHub Classroom has an unstable service regarding repository creation and imports. If your repository fails to create or there are issues with code imports you can do the following steps:
>
> 1. Wait. Sometimes it gets done after 1-2 hours.
> 2. Write to your mentors to do it manually for you.
>
> In the meantime, we are working on an own solution to replace GitHub Classroom. We plan to have it in the first quarter of 2020.

!> This week you need to continue the same repository as the first part of this project, but you'll need to merge a `sprint-2` branch. See the hint above about this.

Click here to clone your own Git repository (this is the same as last week):
https://classroom.github.com/g/PD6sfLga


## Background materials

**SQL:**
- :exclamation: [Installing and setting up PostgreSQL](https://learn.code.cool/full-stack/#/../pages/tools/installing-postgresql.md)
- :exclamation: [Installing psycopg2](https://learn.code.cool/full-stack/#/../pages/tools/installing-psycopg2.md)
- :exclamation: [Best practices for Python/Psycopg/Postgres](https://learn.code.cool/full-stack/#/../pages/python/tips-python-psycopg-postgres)
- [Setting up a database connection in PyCharm](https://learn.code.cool/full-stack/#/../pages/tools/pycharm-database.md)
- [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation)
- :open_book: [PostgreSQL documentation page on Queries](https://www.postgresql.org/docs/current/queries.html)
- :open_book: [PostgreSQL documentation page Data Manipulation](https://www.postgresql.org/docs/current/dml.html)
- [Database glossary](https://learn.code.cool/full-stack/#/../pages/sql/database-glossary.md)

**Agile/SCRUM:**
- [Agile project management](https://learn.code.cool/full-stack/#/../pages/methodology/agile-project-management)
- :open_book: [Planning poker](https://en.wikipedia.org/wiki/Planning_poker)

**Web basics (Flask/Jinja/HTML/CSS):**
- :exclamation: [Flask/Jinja Tips & Tricks](https://learn.code.cool/full-stack/#/../pages/web/web-with-python-tips.md)
- :exclamation: [Passing data from browser](https://learn.code.cool/web-python/#/../pages/web/passing-data-from-browser)
- [Collection of web resources](https://learn.code.cool/full-stack/#/../pages/web/resources.md)
- :open_book: [Pip and VirtualEnv](https://learn.code.cool/full-stack/#/../pages/python/pip-and-virtualenv)
- :open_book: [A web-framework for Python: Flask](https://learn.code.cool/full-stack/#/../pages/python/python-flask)
- :open_book: [Flask documentation](http://flask.palletsprojects.com/) (the Quickstart gives a good overview)
- :open_book: [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)


## Acceptance review

You will need this only at review time, **after** completing the project.
[Use this form](https://forms.gle/fZttAwnTvJ148gcy6) to record the review you provide for your peer.