import pytest

@pytest.mark.parametrize('field, expected_value', [
    ('PRODID', '-//Plönë.org//NONSGML plone.app.event//EN'),
    ('X-WR-CALDESC', 'test non ascii: äöü ÄÖÜ €'),
])
def test_calendar_from_ical_respects_unicode(field, expected_value, calendars):
    cal = calendars.calendar_with_unicode
    assert cal[field].to_ical().decode('utf-8') == expected_value

@pytest.mark.parametrize('test_input, field, expected_value', [
    ('event_with_unicode_fields', 'SUMMARY', 'Non-ASCII Test: ÄÖÜ äöü €'),
    ('event_with_unicode_fields', 'DESCRIPTION', 'icalendar should be able to handle non-ascii: €äüöÄÜÖ.'),
    ('event_with_unicode_fields', 'LOCATION', 'Tribstrül'),
    # Non-unicode characters in summary
    # https://github.com/collective/icalendar/issues/64
    ('issue_64_event_with_non_ascii_summary', 'SUMMARY', 'åäö'),
    # Unicode characters in summary
    ('issue_64_event_with_ascii_summary', 'SUMMARY', 'abcdef'),
])
def test_event_from_ical_respects_unicode(test_input, field, expected_value, events):
    event = events[test_input]
    assert event[field].to_ical().decode('utf-8') == expected_value

def test_events_parameter_unicoded(events):
    '''chokes on umlauts in ORGANIZER
    https://github.com/collective/icalendar/issues/101
    '''
    assert events.issue_101_icalendar_chokes_on_umlauts_in_organizer['ORGANIZER'].params['CN'] == 'acme, ädmin'


def test_broken_property(calendars):
    """
    Test if error messages are encoded properly.
    """
    for event in calendars.broken_ical.walk('vevent'):
        assert len(event.errors) == 1, 'Not the right amount of errors.'
        error = event.errors[0][1]
        assert error.startswith('Content line could not be parsed into parts')


def test_apple_xlocation(calendars):
    """
    Test if we support base64 encoded binary data in parameter values.
    """
    for event in calendars.x_location.walk('vevent'):
        assert len(event.errors) == 0, 'Got too many errors'
