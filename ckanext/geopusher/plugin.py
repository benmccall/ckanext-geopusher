import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model

import pylons.config as config
import pylons

import ckanapi

from ckan.model.domain_object import DomainObjectOperation
from ckan.plugins.toolkit import get_action



class GeopusherPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDomainObjectModification, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'geopusher')

    def notify(self, entity, operation=None):
        if isinstance(entity, model.Resource):
            resource_id = entity.id
            # new event is sent, then a changed event.
            if operation == DomainObjectOperation.changed:
                site_url = config.get('ckan.site_url', 'http://localhost/')
                apikey = model.User.get('default').apikey

                u'''
                Enqueue a background job using RQ (CKAN 2.7+). Fallback to Celery (CKAN 1.5+).
                '''
                try:
                    # Try to use RQ
                    from ckan.plugins.toolkit import enqueue_job
                    enqueue_job(ckanext.geopusher.plugin.process_resource, args=[resource_id, site_url, apikey])
                except ImportError:
                    # Fallback to Celery
                    import uuid
                    from ckan.lib.celery_app import celery
                    celery.send_task(
                        'geopusher.process_resource',
                        args=[resource_id, site_url, apikey],
                        task_id='{}-{}'.format(str(uuid.uuid4()), operation))
