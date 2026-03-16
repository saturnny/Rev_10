"""
Background scheduler for automatic SharePoint synchronization
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import atexit

from .database import SessionLocal
from .sharepoint_sync import run_full_sync, SharePointConfig

# Global scheduler instance
scheduler = None

def init_scheduler():
    """Initialize and start the background scheduler"""
    global scheduler
    
    if scheduler is None:
        scheduler = BackgroundScheduler()
        
        # Add sync job if SharePoint is configured
        if SharePointConfig.is_configured():
            scheduler.add_job(
                func=sync_job,
                trigger=IntervalTrigger(minutes=SharePointConfig.SYNC_INTERVAL),
                id='sharepoint_sync',
                name='SharePoint Synchronization',
                replace_existing=True
            )
        
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())
        
    return scheduler

def sync_job():
    """Background job to run SharePoint sync"""
    print(f"[{datetime.now()}] Starting scheduled SharePoint sync...")
    
    db = SessionLocal()
    try:
        results = run_full_sync(db, direction="export")
        print(f"Sync completed: {results}")
    except Exception as e:
        print(f"Sync error: {e}")
    finally:
        db.close()

def run_sync_now(direction: str = "export") -> dict:
    """Manually trigger a sync operation"""
    db = SessionLocal()
    try:
        results = run_full_sync(db, direction=direction)
        return results
    finally:
        db.close()

def update_sync_interval(minutes: int):
    """Update the sync interval and reschedule"""
    global scheduler
    
    if scheduler:
        # Remove existing job
        try:
            scheduler.remove_job('sharepoint_sync')
        except:
            pass
        
        # Add new job with updated interval
        scheduler.add_job(
            func=sync_job,
            trigger=IntervalTrigger(minutes=minutes),
            id='sharepoint_sync',
            name='SharePoint Synchronization',
            replace_existing=True
        )

def get_scheduler_status():
    """Get current scheduler status"""
    if not scheduler:
        return {"running": False, "jobs": []}
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": str(job.next_run_time) if job.next_run_time else None,
            "trigger": str(job.trigger)
        })
    
    return {
        "running": scheduler.running,
        "jobs": jobs
    }
