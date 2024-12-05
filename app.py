from portal import create_app

app = create_app()

app.config.update(
    SESSION_COOKIE_SAMESITE='strict',
    SESSION_COOKIE_PATH='/',
)

if __name__ == "__main__":
    app.run(port=8000)
