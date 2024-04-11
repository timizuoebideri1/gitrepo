import sys
import time
import uuid

from django.conf import settings
from django.db import transaction

from nautobot.apps.jobs import (
    DryRunVar,
    FileVar,
    IntegerVar,
    Job,
    JobButtonReceiver,
    JobHookReceiver,
    JSONVar,
    register_jobs,
)
from nautobot.dcim.models import Device, Location
from nautobot.extras.choices import ObjectChangeActionChoices
from nautobot.extras.models import Tag

name = "Dean Run Jobs"


class AddNewTagsJob(Job):
    dryrun = DryRunVar()

    class Meta:
        name = "Add New Tags Job"
        description = "Add new Tags."

    def run(self, dryrun):
        try:
            with transaction.atomic():
                tags_to_create = Tag(name=f"Tag From Job {uuid.uuid4().hex[:5]}")
                log_msg = "Creating tag %s."
                if dryrun:
                    log_msg += " (DRYRUN)"
                self.logger.info(log_msg, tags_to_create.name)
                if not dryrun:
                    tags_to_create.save()
        except Exception:
            self.logger.error("%s failed. Database changes rolled back.", self.__name__)
            raise



class AddNewTagsJobHookReceiver(JobHookReceiver):
    class Meta:
        name = "Add new Tag job hook receiver"
        description = "Validate changes to object serial field"

    def receive_job_hook(self, change, action, changed_object):
        # return on delete action
        if action == ObjectChangeActionChoices.ACTION_DELETE:
            return
        
        last_tag = Tag.objects.last()
        if not last_tag or not last_tag.name.startswith("Tag From Job"):
            self.logger.warning("No Tags was created from jobs")
        else:
            last_tag.name = last_tag.name + " (HOOK PASSED)"
            self.logger.info("Last Tag job created successfully has passed check")

register_jobs(AddNewTagsJob, AddNewTagsJobHookReceiver)
