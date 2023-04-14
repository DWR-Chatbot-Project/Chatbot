# CA Water Regulations Chatbot

This repo has been updated to work with `Python v3.8` and up.

## How To Run

1. Install `virtualenv`:

```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and run:

```
$ cd web-frontend/ui
$ virtualenv env
```

3. Then run the command:

```
$ .\env\Scripts\activate
```

4. Then install the dependencies:

```
$ (env) pip install -r requirements.txt
```

5. Finally start the web server:

```
$ (env) python app.py
```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    index=initialize_index("index.json")
    app.run(debug=True, port=<desired port>)
```

## Contributing

Any pull requests that don't address security flaws or fixes for language updates will be automatically closed. Style changes, adding libraries, etc are valid changes for submitting a pull request.

## Tutorials

-   https://buffml.com/web-based-chatbot-using-flask-api/
-   https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
-   https://gpt-index.readthedocs.io/en/latest/guides/tutorials/fullstack_app_guide.html
