from nautobot.core.celery import register_jobs
from jobs.job_module import (GitRepoTrialJob)


register_jobs(GitRepoTrialJob)
# print("XXXXXXXXXXXX IM SKIPPING REG TODAY XXXXXXXXXXXXXXX")