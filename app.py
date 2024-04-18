from src import config, create_app

if __name__ == "__main__":
    app = create_app()    
    app.run(host = config.HOST,
            port = config.PORT,
            debug=config.DEBUG)