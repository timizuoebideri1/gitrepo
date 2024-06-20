# from nautobot.apps.jobs import Job
from nautobot.extras.jobs import Job

class GitRepoTrialJob(Job):
    class Meta:
        name = "Git Repo Trial New Name"
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
