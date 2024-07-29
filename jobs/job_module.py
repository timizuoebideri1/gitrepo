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
        soft_time_limit = 4 * 3600
        time_limit = 4 * 3600
    
    def run(self, data=None, commit=None, **kwargs):
        import time
        ZTP_REDIRECT_MAX_WAIT_MINUTES = 90
        iterator = iter(range(ZTP_REDIRECT_MAX_WAIT_MINUTES))
        while True:
            try:
                self.logger.info("Logged interval message")
                time.sleep(60)
                next(iterator)
            except StopIteration:
                self.logger.info("Wait time exceeded")
                break
        self.logger.info("Continuing...")
