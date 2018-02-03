import cassiopeia

def test_all_fields_work():
    status = cassiopeia.get_status('NA')
    status.hostname
    status.name
    status.region
    status.slug
    for service in status.services:
        service.slug
        service.name
        service.incidents
        service.status
        for incident in service.incidents:
            incident.active
            incident.created
            incident.id
            incident.updates
            for update in incident.updates:
                update.created
                update.author
                update.content
                update.severity
                update.translations
                update.updated
                for translation in update.translations:
                    translation.content
                    translation.locale
                    translation.updated
