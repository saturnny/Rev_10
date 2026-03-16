import uvicorn

if __name__ == "__main__":
    # Seed the database with initial data
    print("Seeding database...")
    from seed_data import seed_database
    seed_database()
    
    # Initialize SharePoint sync scheduler
    print("Initializing SharePoint sync scheduler...")
    from app.scheduler import init_scheduler
    init_scheduler()
    
    # Start the server
    print("Starting server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
