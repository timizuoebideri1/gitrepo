# from nautobot.apps.jobs import Job
from nautobot.extras.jobs import Job

class GitRepoTrialJob(Job):
    class Meta:
        name = "Git Repo Trial New Name"
        description = """
            Markdown Formatting

            *This is italicized*
        """
        soft_time_limit = 1 * 60
        time_limit = 2 * 60
    
    def run(self):
        self.logger.debug("Running for seconds.")
        self.logger.info("Step %s", 4)
        import time
        for i in range(10):
            time.sleep(10)
            self.logger.info(f"I have slept for {i + 10} sec")
        self.logger.info("Im done sleeping")
