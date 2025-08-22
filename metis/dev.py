from server import bootstrap

if __name__ == "__main__":
    app = bootstrap()

    app.run(
        host="0.0.0.0", port=18082, debug=True, auto_reload=False, single_process=True
    )
