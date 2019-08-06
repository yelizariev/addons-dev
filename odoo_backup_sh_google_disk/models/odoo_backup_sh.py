# Copyright 2019 Dinar Gabbasov <https://it-projects.info/team/GabbasovDinar>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import logging
import tempfile
import io
from datetime import datetime

try:
    from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
    from apiclient import errors
except ImportError as err:
    logging.getLogger(__name__).debug(err)

from odoo import api, models, fields
from odoo.addons.odoo_backup_sh.models.odoo_backup_sh import REMOTE_STORAGE_DATETIME_FORMAT
from odoo.addons.odoo_backup_sh.models.odoo_backup_sh import BACKUP_NAME_SUFFIX, BACKUP_NAME_ENCRYPT_SUFFIX
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


_logger = logging.getLogger(__name__)


class BackupConfig(models.Model):
    _inherit = "odoo_backup_sh.config"

    storage_service = fields.Selection(selection_add=[('google_drive', 'Google Drive')])

    @api.model
    def get_backup_list(self, cloud_params):
        backup_list = super(BackupConfig, self).get_backup_list(cloud_params) or dict()
        # get all backups from Google Drive
        GoogleDriveService = self.env['ir.config_parameter'].get_google_drive_service()
        if not GoogleDriveService:
            return {}
        folder_id = self.env['ir.config_parameter'].get_param("odoo_backup_sh_google_disk.google_disk_folder_id")
        response = GoogleDriveService.files().list(q="'" + folder_id + "' in parents",
                                                   fields="nextPageToken, files(id, name)",
                                                   spaces="drive").execute()
        google_drive_backup_list = [(r.get('name'), 'google_drive') for r in response.get('files', [])]
        if 'backup_list' in backup_list:
            backup_list.update({
                'backup_list': backup_list['backup_list'] + google_drive_backup_list
            })
        else:
            backup_list['backup_list'] = google_drive_backup_list
        return backup_list

    @api.model
    def get_info_file_object(self, cloud_params, info_file_name, storage_service):
        if storage_service == 'google_drive':
            GoogleDriveService = self.env['ir.config_parameter'].get_google_drive_service()
            file_id = self.get_google_drive_file_id(info_file_name)
            if file_id:
                fh = io.BytesIO()
                request = GoogleDriveService.files().get_media(fileId=file_id)
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                fh.seek(0)
                return fh
        else:
            return super(BackupConfig, self).get_info_file_object(cloud_params, info_file_name, storage_service)

    @api.model
    def get_google_drive_file_id(self, file_name):
        GoogleDriveService = self.env['ir.config_parameter'].get_google_drive_service()
        folder_id = self.env['ir.config_parameter'].get_param("odoo_backup_sh_google_disk.google_disk_folder_id")
        response = GoogleDriveService.files().list(
            q="'" + folder_id + "' in parents and name = '" + file_name + "'",
            fields="nextPageToken, files(id)",
            spaces="drive").execute()
        file = response.get('files', [])
        return file[0].get('id')

    @api.model
    def create_info_file(self, info_file_object, storage_service):
        if storage_service == 'google_drive':
            info_file_object.seek(0)
            info_file = tempfile.NamedTemporaryFile()
            info_file.write(info_file_object.read())
            info_file.seek(0)
            return info_file
        else:
            return super(BackupConfig, self).create_info_file(info_file_object, storage_service)

    @api.model
    def delete_remote_objects(self, cloud_params, remote_objects):
        GoogleDriveService = self.env['ir.config_parameter'].get_google_drive_service()
        google_drive_remove_objects = []
        for file in remote_objects:
            if file[1] == 'google_drive':
                google_drive_remove_objects.append(file)
                file_id = self.get_google_drive_file_id(file[0])
                try:
                    GoogleDriveService.files().delete(fileId=file_id).execute()
                except errors.HttpError as e:
                    _logger.exception(e)
        return super(BackupConfig, self).delete_remote_objects(cloud_params, list(set(remote_objects) - set(google_drive_remove_objects)))

    @api.model
    def make_backup_google_drive(self, ts, name, dump_stream, info_file, info_file_content, cloud_params):
        # Upload two backup objects to Google Drive
        GoogleDriveService = self.env['ir.config_parameter'].get_google_drive_service()
        folder_id = self.env['ir.config_parameter'].get_param("odoo_backup_sh_google_disk.google_disk_folder_id")
        db_metadata = {
            "name": "%s.%s%s" % (name, ts, BACKUP_NAME_ENCRYPT_SUFFIX if info_file_content.get('encrypted') else BACKUP_NAME_SUFFIX),
            "parents": [folder_id],
        }
        info_metadata = {
            "name": "%s.%s%s" % (name, ts, '.info'),
            "parents": [folder_id],
        }
        db_mimetype = "application/zip"
        info_mimetype = "text/plain"
        dump_stream.seek(0)
        info_file.seek(0)
        for obj, mimetype, metadata in [[dump_stream, db_mimetype, db_metadata],
                                        [info_file, info_mimetype, info_metadata]]:
            media = MediaIoBaseUpload(obj, mimetype, resumable=True)
            GoogleDriveService.files().create(body=metadata, media_body=media, fields="id").execute()


class BackupInfo(models.Model):
    _inherit = 'odoo_backup_sh.backup_info'

    storage_service = fields.Selection(selection_add=[('google_drive', 'Google Drive')])


class BackupRemoteStorage(models.Model):
    _inherit = 'odoo_backup_sh.remote_storage'

    google_drive_used_remote_storage = fields.Integer(string='Google Drive Usage, MB', readonly=True)

    @api.multi
    def compute_total_used_remote_storage(self):
        self.compute_google_drive_used_remote_storage()
        super(BackupRemoteStorage, self).compute_total_used_remote_storage()

    @api.multi
    def compute_google_drive_used_remote_storage(self):
        amount = sum(self.env['odoo_backup_sh.backup_info'].search([('storage_service', '=', 'google_drive')]).mapped('backup_size'))
        today_record = self.search([('date', '=', datetime.strftime(datetime.now(), DEFAULT_SERVER_DATE_FORMAT))])
        if today_record:
            today_record.google_drive_used_remote_storage = amount
        else:
            self.create({
                'date': datetime.now(),
                'google_drive_used_remote_storage': amount
            })


class DeleteRemoteBackupWizard(models.TransientModel):
    _inherit = "odoo_backup_sh.delete_remote_backup_wizard"

    @api.multi
    def delete_remove_backup_button(self):
        record_ids = (self._context.get('active_model') == 'odoo_backup_sh.backup_info' and self._context.get('active_ids') or [])
        backup_info_records = self.env['odoo_backup_sh.backup_info'].search([('id', 'in', record_ids)])
        GoogleDriveService = self.env['ir.config_parameter'].get_google_drive_service()
        backup_google_drive_info_records = backup_info_records.filtered(lambda r: r.storage_service == 'google_drive')
        for record in backup_google_drive_info_records:
            backup_files_suffixes = ['.zip', '.info']
            if record.encrypted:
                backup_files_suffixes[0] += '.enc'
            upload_datetime = datetime.strftime(record.upload_datetime, REMOTE_STORAGE_DATETIME_FORMAT)
            for suffix in backup_files_suffixes:
                obj_name = "%s.%s%s" % (record.database, upload_datetime, suffix)
                file_id = self.env["odoo_backup_sh.config"].get_google_drive_file_id(obj_name)
                try:
                    GoogleDriveService.files().delete(fileId=file_id).execute()
                except errors.HttpError as e:
                    _logger.exception(e)
        backup_google_drive_info_records.unlink()
        super(DeleteRemoteBackupWizard, self).delete_remove_backup_button()
