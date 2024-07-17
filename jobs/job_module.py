# from nautobot.apps.jobs import Job
from nautobot.extras.jobs import Job

class GitRepoTrialJob(Job):
    class Meta:
        name = "Git Repo Trial New Name"
        description = """
            Markdown Formatting

            *This is italicized*
        """
        has_sensitive_variables = False
        soft_time_limit = 40
        time_limit = 60
    
    def run(self, data=None, commit=None, **kwargs):
        self.logger.debug("Running for seconds.")
        self.logger.info("Step %s", 4)
        import time
        for i in range(10):
            time.sleep(5)
            self.logger.info(f"I have slept for {(i + 1) * 5} sec")
        self.logger.info("Im done sleeping")
