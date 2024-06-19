from nautobot.core.celery import register_jobs
# from .job_module import (GitRepoTrialJob)
from nautobot.extras.jobs import Job

class GitRepoTrialJob(Job):
    class Meta:
        name = "Git Repo Trial Jobs 5"
        description = """
            Markdown Formatting

            *This is italicized*
        """
        # soft_time_limit = 15 * 60
    
    def run(self):
        # self.logger.debug("Running for %s seconds.", interval)
        self.logger.info("Step %s", 4)
        import time
        for i in range(10):
            time.sleep(60)
            self.logger.info(f"I have slept for {i} min")
        self.logger.info("Im done sleeping")
        
register_jobs(GitRepoTrialJob)
# print("XXXXXXXXXXXX IM SKIPPING REG TODAY XXXXXXXXXXXXXXX")