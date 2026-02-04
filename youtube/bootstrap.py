def bootstrap_jobs():
    from youtube.scheduler import scheduler
    from youtube.jobs import register_youtube_job
    from lead.services.register_followup_job import register_followup_job

    register_youtube_job(scheduler)
    register_followup_job(scheduler)
