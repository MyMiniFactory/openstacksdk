# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack import format
from openstack import resource
from openstack import utils


class Volume(resource.Resource):
    resource_key = "volume"
    resources_key = "volumes"
    base_path = "/volumes"

    _query_mapping = resource.QueryParameters(
        'name', 'status', 'project_id', all_projects='all_tenants')

    # capabilities
    allow_fetch = True
    allow_create = True
    allow_delete = True
    allow_commit = True
    allow_list = True

    # Properties
    #: TODO(briancurtin): This is currently undocumented in the API.
    attachments = resource.Body("attachments")
    #: The availability zone.
    availability_zone = resource.Body("availability_zone")
    #: ID of the consistency group.
    consistency_group_id = resource.Body("consistencygroup_id")
    #: The timestamp of this volume creation.
    created_at = resource.Body("created_at")
    #: The volume description.
    description = resource.Body("description")
    #: Extended replication status on this volume.
    extended_replication_status = resource.Body(
        "os-volume-replication:extended_status")
    #: The volume's current back-end.
    host = resource.Body("os-vol-host-attr:host")
    #: The ID of the image from which you want to create the volume.
    #: Required to create a bootable volume.
    image_id = resource.Body("imageRef")
    #: Enables or disables the bootable attribute. You can boot an
    #: instance from a bootable volume. *Type: bool*
    is_bootable = resource.Body("bootable", type=format.BoolStr)
    #: ``True`` if this volume is encrypted, ``False`` if not.
    #: *Type: bool*
    is_encrypted = resource.Body("encrypted", type=format.BoolStr)
    #: One or more metadata key and value pairs to associate with the volume.
    metadata = resource.Body("metadata")
    #: The volume ID that this volume's name on the back-end is based on.
    migration_id = resource.Body("os-vol-mig-status-attr:name_id")
    #: The status of this volume's migration (None means that a migration
    #: is not currently in progress).
    migration_status = resource.Body("os-vol-mig-status-attr:migstat")
    #: The project ID associated with current back-end.
    project_id = resource.Body("os-vol-tenant-attr:tenant_id")
    #: Data set by the replication driver
    replication_driver_data = resource.Body(
        "os-volume-replication:driver_data")
    #: Status of replication on this volume.
    replication_status = resource.Body("replication_status")
    #: Scheduler hints for the volume
    scheduler_hints = resource.Body('OS-SCH-HNT:scheduler_hints', type=dict)
    #: The size of the volume, in GBs. *Type: int*
    size = resource.Body("size", type=int)
    #: To create a volume from an existing snapshot, specify the ID of
    #: the existing volume snapshot. If specified, the volume is created
    #: in same availability zone and with same size of the snapshot.
    snapshot_id = resource.Body("snapshot_id")
    #: To create a volume from an existing volume, specify the ID of
    #: the existing volume. If specified, the volume is created with
    #: same size of the source volume.
    source_volume_id = resource.Body("source_volid")
    #: One of the following values: creating, available, attaching, in-use
    #: deleting, error, error_deleting, backing-up, restoring-backup,
    #: error_restoring. For details on these statuses, see the
    #: Block Storage API documentation.
    status = resource.Body("status")
    #: The user ID associated with the volume
    user_id = resource.Body("user_id")
    #: One or more metadata key and value pairs about image
    volume_image_metadata = resource.Body("volume_image_metadata")
    #: The name of the associated volume type.
    volume_type = resource.Body("volume_type")

    def _action(self, session, body):
        """Preform volume actions given the message body."""
        # NOTE: This is using Volume.base_path instead of self.base_path
        # as both Volume and VolumeDetail instances can be acted on, but
        # the URL used is sans any additional /detail/ part.
        url = utils.urljoin(Volume.base_path, self.id, 'action')
        headers = {'Accept': ''}
        return session.post(url, json=body, headers=headers)

    def extend(self, session, size):
        """Extend a volume size."""
        body = {'os-extend': {'new_size': size}}
        self._action(session, body)

    def set_readonly(self, session, readonly):
        """Set volume readonly flag"""
        body = {'os-update_readonly_flag': {'readonly': readonly}}
        self._action(session, body)

    def retype(self, session, new_type, migration_policy):
        """Retype volume considering the migration policy"""
        body = {
            'os-retype': {
                'new_type': new_type,
                'migration_policy': migration_policy
            }
        }
        self._action(session, body)


VolumeDetail = Volume
