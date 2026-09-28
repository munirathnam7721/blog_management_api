from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.database.connection import SessionLocal
from app.models.post import Post


# ============================================================
# CREATE SCHEDULER
# ============================================================

scheduler = BackgroundScheduler()


# ============================================================
# AUTOMATIC PUBLISHING JOB
# ============================================================

def publish_scheduled_posts():

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # FIND POSTS WHOSE SCHEDULED TIME HAS ARRIVED
        # ----------------------------------------------------

        posts = db.query(
            Post
        ).filter(
            Post.status == "scheduled",
            Post.scheduled_at <= datetime.utcnow()
        ).all()

        # ----------------------------------------------------
        # PUBLISH EACH POST
        # ----------------------------------------------------

        for post in posts:

            post.status = "published"

            post.published_at = datetime.utcnow()

            post.scheduled_at = None

        # ----------------------------------------------------
        # SAVE CHANGES
        # ----------------------------------------------------

        if posts:

            db.commit()

            print(
                f"Published {len(posts)} scheduled post(s)"
            )

    except Exception as error:

        db.rollback()

        print(
            "Error while publishing scheduled posts:",
            error
        )

    finally:

        db.close()


# ============================================================
# START SCHEDULER
# ============================================================

def start_scheduler():

    if not scheduler.running:

        scheduler.add_job(
            publish_scheduled_posts,
            "interval",
            minutes=1,
            id="publish_scheduled_posts",
            replace_existing=True
        )

        scheduler.start()

        print(
            "Scheduled post publisher started."
        )


# ============================================================
# STOP SCHEDULER
# ============================================================

def stop_scheduler():

    if scheduler.running:

        scheduler.shutdown()

        print(
            "Scheduled post publisher stopped."
        )