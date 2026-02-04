def register_followup_job(scheduler):
    from .followup_job import followup_job

    scheduler.add_job(
        followup_job,
        trigger="interval",
        minutes=1,
        id="dm_followup_job",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
