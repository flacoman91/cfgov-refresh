import json
import logging
import os

from django.core.management.base import BaseCommand

from v1.models.browse_page import BrowsePage
from v1.tests.wagtail_pages.helpers import publish_changes


logger = logging.getLogger(__name__)

# check if inquiry index or credit tightness chart
def matches_prefix(prefix, data_source):
    if prefix in data_source:
        print prefix + ' is in ' + data_source
        return True
    else:
        return False

def get_inquiry_month(data, data_source):
    for item in data:
        # if inquiry month, the month is inquiry month OR credit tightness month.
        # does the market match the data_source?
        # is the data source inq_ (inquiry index) or crt_(credit tightness)?
        month = '2033-03-03'
        if 'inquiry_month' in item:
            month = '2022-02-02'
            if item['market_key'] in data_source:
                month = '2021-01-01'
                if matches_prefix('inq_', data_source):
                    month = item['inquiry_month']
                    break
                elif matches_prefix('crt_', data_source):
                    month = item['tightness_month']
                    break
    return month

class Command(BaseCommand):
    help = 'Monthly updates to data snapshot values'

    def expand_path(self, path):
        """Expands a relative path into an absolute path"""
        rootpath = os.path.abspath(os.path.expanduser(path))

        return rootpath

    def add_arguments(self, parser):
        """Adds all arguments to be processed."""
        parser.add_argument(
            '--snapshot_file',
            required=True,
            help='JSON file containing all markets\' data snapshot values'
        )

    def update_chart_blocks(self, date_published, last_updated, markets):
        """ Update date_published on all chart blocks """

        for page in BrowsePage.objects.all():
            chart_blocks = filter(
                lambda item: item['type'] == 'chart_block',
                page.specific.content.stream_data
            )
            if not chart_blocks:
                continue
            for chart in chart_blocks:
                chart['value']['date_published'] = date_published
                if chart['value']['chart_type'] == 'line-index':
                    last_updated_inquiry = get_inquiry_month(markets, chart['value']['data_source'])
                    chart['value']['last_updated_projected_data'] = last_updated_inquiry
                else:
                    chart['value']['last_updated_projected_data'] = last_updated
            publish_changes(page.specific)

    def handle(self, *args, **options):
        # Read in CCT snapshot data from json file
        with open(self.expand_path(options['snapshot_file'])) as json_data:
            data = json.load(json_data)

        markets = data['markets']
        date_published = data['date_published']
        last_updated = max(
            [item['data_month'] for item in markets]
        )

        self.update_chart_blocks(date_published, last_updated, markets)
