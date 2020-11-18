# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: Red Hat Inc. 2020
# Authors: Willian Rampazzo <willianr@redhat.com>

"""
Requirements Resolver module.
"""

from ..nrunner import Runnable, Task, RUNNERS_REGISTRY_PYTHON_CLASS

SUPPORTED_REQUIREMENTS = {}


def create_requirements_tasks(tasks):
    """Entry point for the Requirements Resolver.

    This function isolates the Requirements Resolver object into this module.

    :param tasks: List of tasks
    :type tasks: list
    """
    resolver = RequirementsResolver(tasks)
    return resolver.create_requirements_tasks()

class UnsupportedRequirementType(Exception):
    pass

class RequirementsResolver:
    """
    """

    def __init__(self, tasks):
        """
        """
        self._tasks = tasks

    def create_requirements_tasks(self):
        """
        """
        print(" == Requirement Resolver Input Tasks: %s" % self._tasks)

        requirements_tasks = []
        for task in self._tasks:
            if not task.runnable.requirements:
                continue

            uris = [status_service.uri
                    for status_service in task.status_services]

            for requirement in task.runnable.requirements:
                try:
                    type_klass = SUPPORTED_REQUIREMENTS[requirement['type']]
                except KeyError:
                    # ignore while in draft
                    print("Requirement type not supported: %s" %requirement['type'])
                    continue
                    #raise UnsupportedRequirementType

                type_resolver = type_klass(requirement, uris)
                requirement_task = type_resolver.task_from_requirement()
                requirements_tasks.append(requirement_task)
                task.prereqs.append(requirement_task.uid)
        self._tasks.extend(requirements_tasks)
        return self._tasks

class BaseRequirement:
    """Base interface for a requirement type."""

    def __init__(self, requirement, uris):
        """
        """
        self._requirement = requirement
        self._uris = uris

    def task_from_requirement(self):
        """
        """
        raise NotImplementedError

class PackageRequirement(BaseRequirement):
    """
    """

    def task_from_requirement(self):
        """
        """
        print('Creating package task: %s' % self._requirement)
        # change the argument to 'install' after draft
        runnable = Runnable('requirement', 'avocado-software-manager',
                            'check-installed',
                            self._requirement['name'])
        # need to decide how to handle ids and logs
        task_id = 'requirement-%s-%s' % (self._requirement['type'],
                                         self._requirement['name'])
        task = Task(task_id, runnable,
                    status_uris=self._uris,
                    known_runners=RUNNERS_REGISTRY_PYTHON_CLASS)

        return task

SUPPORTED_REQUIREMENTS['package'] = PackageRequirement
