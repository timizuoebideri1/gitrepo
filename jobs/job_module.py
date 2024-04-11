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

class ExampleJobHookReceiver(JobHookReceiver):
    class Meta:
        name = "Example job hook receiver"
        description = "Validate changes to object serial field"

    def receive_job_hook(self, change, action, changed_object):
        # return on delete action
        if action == ObjectChangeActionChoices.ACTION_DELETE:
            return

        # log diff output
        snapshots = change.get_snapshots()
        self.logger.info("DIFF: %s", snapshots["differences"])

        # validate changes to serial field
        if "serial" in snapshots["differences"]["added"]:
            old_serial = snapshots["differences"]["removed"]["serial"]
            new_serial = snapshots["differences"]["added"]["serial"]
            self.logger.info("%s serial has been changed from %s to %s", changed_object, old_serial, new_serial)

            # Check the new serial is valid and revert if necessary
            if not self.validate_serial(new_serial):
                changed_object.serial = old_serial
                changed_object.save()
                self.logger.info("%s serial %s was not valid. Reverted to %s", changed_object, new_serial, old_serial)

            self.logger.info("Serial validation completed for %s", changed_object)

    def validate_serial(self, serial):
        # add business logic to validate serial
        return False

register_jobs(GitRepoJob, ExampleJobHookReceiver)
