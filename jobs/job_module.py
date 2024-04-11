import sys
import time

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

name = "Git Repo Job"


class GitRepoJob(Job):
    dryrun = DryRunVar()

    class Meta:
        name = "Git Repo Dry Run"
        approval_required = True
        has_sensitive_variables = False
        description = "Example job to remove serial number on all devices, supports dryrun mode."

    def run(self, dryrun):
        try:
            with transaction.atomic():
                devices_with_serial = Device.objects.exclude(serial="")
                log_msg = "Removing serial on %s devices."
                if dryrun:
                    log_msg += " (DRYRUN)"
                self.logger.info(log_msg, devices_with_serial.count())
                for device in devices_with_serial:
                    if not dryrun:
                        device.serial = ""
                        device.save()
        except Exception:
            self.logger.error("%s failed. Database changes rolled back.", self.__name__)
            raise

register_jobs(GitRepoJob)
