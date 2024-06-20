from nautobot.core.celery import register_jobs
from gitrepo.jobs.job_module import (GitRepoTrialJob)


register_jobs(GitRepoTrialJob)
# print("XXXXXXXXXXXX IM SKIPPING REG TODAY XXXXXXXXXXXXXXX")