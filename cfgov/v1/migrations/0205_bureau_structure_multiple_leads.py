"""
Convert BureauStructure block data from this schema:

{
    'last_updated_date': datetime.date,
    'download_image': <primary key to Wagtail document>
    'director': string,
    'divisions': [
        {
            'division': string,
            'division_lead': string,
            'title': {
                'line_1': string,
                'line_2': string,
            },
            'division_lead_1': string,
            'title_1': {
                'line_1': string,
                'line_2': string,
            },
            'link_to_division_page': {
                'text': string,
                'url': string,
            },
            'offices': [
                {
                    'office_name': string,
                    'lead': string,
                    'title': {
                        'line_1': string,
                        'line_2': string,
                    },
                },
                ...
            ],
        },
        ...
    ],
    'office_of_the_director': [
        {
            'office_name': string,
            'lead': string,
            'title': {
                'line_1': string,
                'line_2': string,
            },
            'offices': [
                {
                    'office_name': string,
                    'lead': string,
                    'title': {
                        'line_1': string,
                        'line_2': string,
                    },
                },
                ...
            ],
        },
        ...
    ],
}

to this schema:

{
    'last_updated_date': datetime.date,
    'download_image': <primary key to Wagtail document>
    'director': string,
    'divisions': [
        {
            'name': string,
            'leads': [
                {
                    'name': string,
                    'title': string,
                },
                ...
            ],
            'overview_page': string,
            'offices': [
                {
                    'name': string,
                    'leads': [
                        {
                            'name': string,
                            'title': string,
                        },
                        ...
                    ],
                },
                ...
            ],
        },
        ...
    ],
    'office_of_the_director': [
        {
            'name': string,
            'leads': [
                {
                    'name': string,
                    'title': string,
                },
                ...
            ],
            'offices': [
                {
                    'name': string,
                    'leads': [
                        {
                            'name': string,
                            'title': string,
                        },
                        ...
                    ],
                },
                ...
            ],
        },
        ...
    ],
}
"""
# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-28 17:29

import django.core.validators
from django.db import migrations
import v1.atomic_elements.organisms
import v1.blocks

try:
    import wagtail.wagtailcore.blocks as core_blocks
    import wagtail.wagtailcore.fields as core_fields
    import wagtail.wagtaildocs.blocks as docs_blocks
    import wagtail.wagtailimages.blocks as images_blocks
except ImportError:  # pragma: no cover; fallback for Wagtail < 2.0
    import wagtail.core.blocks as core_blocks
    import wagtail.core.fields as core_fields
    import wagtail.documents.blocks as docs_blocks
    import wagtail.images.blocks as images_blocks


from v1.util.migrations import migrate_page_types_and_fields


def mapper(page_or_revision, value):
    divisions = value.get('divisions')
    office_of_the_director = value.get('office_of_the_director')

    if divisions:
        migrated_divisions = []

        for division in divisions:
            leads = []
            for suffix in ('', '_1'):
                name = division.get('division_lead' + suffix)
                if name:
                    title = division.get('title' + suffix, {})
                    leads.append({
                        'name': name,
                        'title': '\n'.join(filter(None, [
                            title['line_1'],
                            title['line_2']
                        ])),
                    })

            migrated_divisions.append({
                'name': division['division'],
                'leads': leads,
                'offices': [
                    {
                        'name': office['office_name'],
                        'leads': [
                            {
                                'name': office['lead'],
                                'title': '\n'.join(filter(None, [
                                    office['title']['line_1'],
                                    office['title']['line_2'],
                                ])),
                            },
                        ],
                    } for office in division['offices']
                ],
                'overview_page': division['link_to_division_page']['url'],
            })

        value['divisions'] = migrated_divisions

    if office_of_the_director:
        value['office_of_the_director'] = [
            {
                'name': office['office_name'],
                'leads': [
                    {
                        'name': office['lead'],
                        'title': '\n'.join(filter(None, [
                            office['title']['line_1'],
                            office['title']['line_2'],
                        ])),
                    },
                ],
                'offices': [
                    {
                        'name': sub_office['office_name'],
                        'leads': [
                            {
                                'name': sub_office['lead'],
                                'title': '\n'.join(filter(None, [
                                    sub_office['title']['line_1'],
                                    sub_office['title']['line_2'],
                                ])),
                            }
                        ] 
                    } for sub_office in office['offices']
                ],
            } for office in office_of_the_director
        ]

    return value


def migrate_forwards(apps, schema_editor):
    migrate_page_types_and_fields(
        apps,
        [('v1', 'BrowsePage', 'content', 'bureau_structure')],
        mapper
    )


def migrate_backwards(apps, schema_editor):
    raise NotImplementedError


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0204_remove_menu_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='browsepage',
            name='content',
            field=core_fields.StreamField((('full_width_text', core_blocks.StreamBlock((('content', core_blocks.RichTextBlock(icon='edit')), ('content_with_anchor', core_blocks.StructBlock((('content_block', core_blocks.RichTextBlock()), ('anchor_link', core_blocks.StructBlock((('link_id', core_blocks.CharBlock(help_text='\n            ID will be auto-generated on save.\n            However, you may enter some human-friendly text that\n            will be incorporated to make it easier to read.\n        ', label='ID for this content block', required=False)),)))))), ('heading', core_blocks.StructBlock((('text', v1.blocks.HeadingTextBlock(required=False)), ('level', core_blocks.ChoiceBlock(choices=[('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')])), ('icon', v1.blocks.HeadingIconBlock(help_text='Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/capital-framework/components/cf-icons/#the-icons">See full list of icons</a>', required=False))), required=False)), ('image', core_blocks.StructBlock((('image', core_blocks.StructBlock((('upload', images_blocks.ImageChooserBlock(required=False)), ('alt', core_blocks.CharBlock(help_text="If the image is decorative (i.e., if a screenreader wouldn't have anything useful to say about it), leave the Alt field blank.", required=False))))), ('image_width', core_blocks.ChoiceBlock(choices=[('full', 'full'), (470, '470px'), (270, '270px'), (170, '170px')])), ('image_position', core_blocks.ChoiceBlock(choices=[('right', 'right'), ('left', 'left')], help_text='Does not apply if the image is full-width')), ('text', core_blocks.RichTextBlock(label='Caption', required=False)), ('is_bottom_rule', core_blocks.BooleanBlock(default=True, help_text='Check to add a horizontal rule line to bottom of inset.', label='Has bottom rule line', required=False))))), ('table_block', v1.atomic_elements.organisms.AtomicTableBlock(table_options={'renderer': 'html'})), ('quote', core_blocks.StructBlock((('body', core_blocks.TextBlock()), ('citation', core_blocks.TextBlock(required=False)), ('is_large', core_blocks.BooleanBlock(required=False))))), ('cta', core_blocks.StructBlock((('slug_text', core_blocks.CharBlock(required=False)), ('paragraph_text', core_blocks.RichTextBlock(required=False)), ('button', core_blocks.StructBlock((('text', core_blocks.CharBlock(required=False)), ('url', core_blocks.CharBlock(default='/', required=False)), ('size', core_blocks.ChoiceBlock(choices=[('regular', 'Regular'), ('large', 'Large Primary')])))))))), ('related_links', core_blocks.StructBlock((('heading', core_blocks.CharBlock(required=False)), ('paragraph', core_blocks.RichTextBlock(required=False)), ('links', core_blocks.ListBlock(core_blocks.StructBlock((('text', core_blocks.CharBlock(required=False)), ('url', core_blocks.CharBlock(default='/', required=False))))))))), ('reusable_text', v1.blocks.ReusableTextChooserBlock('v1.ReusableText')), ('email_signup', core_blocks.StructBlock((('heading', core_blocks.CharBlock(default='Stay informed', required=False)), ('default_heading', core_blocks.BooleanBlock(default=True, help_text='If selected, heading will be styled as an H5 with green top rule. Deselect to style header as H3.', label='Default heading style', required=False)), ('text', core_blocks.CharBlock(help_text='Write a sentence or two about what kinds of emails the user is signing up for, how frequently they will be sent, etc.', required=False)), ('gd_code', core_blocks.CharBlock(help_text='Code for the topic (i.e., mailing list) you want people who submit this form to subscribe to. Format: USCFPB_###', label='GovDelivery code', required=False)), ('disclaimer_page', core_blocks.PageChooserBlock(help_text='Choose the page that the "See Privacy Act statement" link should go to. If in doubt, use "Generic Email Sign-Up Privacy Act Statement".', label='Privacy Act statement', required=False))))), ('well', core_blocks.StructBlock((('content', core_blocks.RichTextBlock(label='Well', required=False)),))), ('well_with_ask_search', core_blocks.StructBlock((('content', core_blocks.RichTextBlock(label='Well', required=False)), ('ask_search', core_blocks.StructBlock((('show_label', core_blocks.BooleanBlock(default=True, help_text='Whether to show form label.', required=False)), ('placeholder', core_blocks.TextBlock(help_text='Text to show for the input placeholder text.', required=False))))))))))), ('info_unit_group', core_blocks.StructBlock((('format', core_blocks.ChoiceBlock(choices=[('50-50', '50/50'), ('33-33-33', '33/33/33'), ('25-75', '25/75')], help_text='Choose the number and width of info unit columns.', label='Format')), ('heading', core_blocks.StructBlock((('text', v1.blocks.HeadingTextBlock(required=False)), ('level', core_blocks.ChoiceBlock(choices=[('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')])), ('icon', v1.blocks.HeadingIconBlock(help_text='Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/capital-framework/components/cf-icons/#the-icons">See full list of icons</a>', required=False))), required=False)), ('intro', core_blocks.RichTextBlock(help_text='If this field is not empty, the Heading field must also be set.', required=False)), ('link_image_and_heading', core_blocks.BooleanBlock(default=True, help_text="Check this to link all images and headings to the URL of the first link in their unit's list, if there is a link.", required=False)), ('has_top_rule_line', core_blocks.BooleanBlock(default=False, help_text='Check this to add a horizontal rule line to top of info unit group.', required=False)), ('lines_between_items', core_blocks.BooleanBlock(default=False, help_text='Check this to show horizontal rule lines between info units.', label='Show rule lines between items', required=False)), ('info_units', core_blocks.ListBlock(core_blocks.StructBlock((('image', core_blocks.StructBlock((('upload', images_blocks.ImageChooserBlock(required=False)), ('alt', core_blocks.CharBlock(help_text="If the image is decorative (i.e., if a screenreader wouldn't have anything useful to say about it), leave the Alt field blank.", required=False))))), ('heading', core_blocks.StructBlock((('text', v1.blocks.HeadingTextBlock(required=False)), ('level', core_blocks.ChoiceBlock(choices=[('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')])), ('icon', v1.blocks.HeadingIconBlock(help_text='Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/capital-framework/components/cf-icons/#the-icons">See full list of icons</a>', required=False))), default={'level': 'h3'}, required=False)), ('body', core_blocks.RichTextBlock(blank=True, required=False)), ('links', core_blocks.ListBlock(core_blocks.StructBlock((('text', core_blocks.CharBlock(required=False)), ('url', core_blocks.CharBlock(default='/', required=False)))), required=False)))))), ('sharing', core_blocks.StructBlock((('shareable', core_blocks.BooleanBlock(help_text='If checked, share links will be included below the items.', label='Include sharing links?', required=False)), ('share_blurb', core_blocks.CharBlock(help_text='Sets the tweet text, email subject line, and LinkedIn post text.', required=False)))))))), ('expandable_group', core_blocks.StructBlock((('heading', core_blocks.CharBlock(help_text='Added as an <code>&lt;h3&gt;</code> at the top of this block. Also adds a wrapping <code>&lt;div&gt;</code> whose <code>id</code> attribute comes from a slugified version of this heading, creating an anchor that can be used when linking to this part of the page.', required=False)), ('body', core_blocks.RichTextBlock(required=False)), ('is_accordion', core_blocks.BooleanBlock(required=False)), ('has_top_rule_line', core_blocks.BooleanBlock(default=False, help_text='Check this to add a horizontal rule line to top of expandable group.', required=False)), ('expandables', core_blocks.ListBlock(core_blocks.StructBlock((('label', core_blocks.CharBlock(required=False)), ('is_bordered', core_blocks.BooleanBlock(required=False)), ('is_midtone', core_blocks.BooleanBlock(required=False)), ('is_expanded', core_blocks.BooleanBlock(required=False)), ('content', core_blocks.StreamBlock((('paragraph', core_blocks.RichTextBlock(required=False)), ('well', core_blocks.StructBlock((('content', core_blocks.RichTextBlock(label='Well', required=False)),))), ('links', core_blocks.StructBlock((('text', core_blocks.CharBlock(required=False)), ('url', core_blocks.CharBlock(default='/', required=False))))), ('email', core_blocks.StructBlock((('emails', core_blocks.ListBlock(core_blocks.StructBlock((('url', core_blocks.EmailBlock(label='Email address')), ('text', core_blocks.CharBlock(label='Link text (optional)', required=False)))))),))), ('phone', core_blocks.StructBlock((('fax', core_blocks.BooleanBlock(default=False, label='Is this number a fax?', required=False)), ('phones', core_blocks.ListBlock(core_blocks.StructBlock((('number', core_blocks.CharBlock(help_text='Do not include spaces or dashes. Ex. 8554112372', max_length=15, validators=[django.core.validators.RegexValidator(message='Enter a numeric phone number, without punctuation.', regex='^\\d*$')])), ('extension', core_blocks.CharBlock(max_length=4, required=False)), ('vanity', core_blocks.CharBlock(help_text='A phoneword version of the above number. Include any formatting. Ex. (555) 222-CFPB', max_length=15, required=False)), ('tty', core_blocks.CharBlock(help_text='Do not include spaces or dashes. Ex. 8554112372', label='TTY', max_length=15, required=False, validators=[django.core.validators.RegexValidator(message='Enter a numeric phone number, without punctuation.', regex='^\\d*$')])), ('tty_ext', core_blocks.CharBlock(label='TTY Extension', max_length=4, required=False))))))))), ('address', core_blocks.StructBlock((('label', core_blocks.CharBlock(required=False)), ('title', core_blocks.CharBlock(required=False)), ('street', core_blocks.CharBlock(required=False)), ('city', core_blocks.CharBlock(max_length=50, required=False)), ('state', core_blocks.CharBlock(max_length=25, required=False)), ('zip_code', core_blocks.CharBlock(max_length=15, required=False)))))), blank=True))))))))), ('expandable', core_blocks.StructBlock((('label', core_blocks.CharBlock(required=False)), ('is_bordered', core_blocks.BooleanBlock(required=False)), ('is_midtone', core_blocks.BooleanBlock(required=False)), ('is_expanded', core_blocks.BooleanBlock(required=False)), ('content', core_blocks.StreamBlock((('paragraph', core_blocks.RichTextBlock(required=False)), ('well', core_blocks.StructBlock((('content', core_blocks.RichTextBlock(label='Well', required=False)),))), ('links', core_blocks.StructBlock((('text', core_blocks.CharBlock(required=False)), ('url', core_blocks.CharBlock(default='/', required=False))))), ('email', core_blocks.StructBlock((('emails', core_blocks.ListBlock(core_blocks.StructBlock((('url', core_blocks.EmailBlock(label='Email address')), ('text', core_blocks.CharBlock(label='Link text (optional)', required=False)))))),))), ('phone', core_blocks.StructBlock((('fax', core_blocks.BooleanBlock(default=False, label='Is this number a fax?', required=False)), ('phones', core_blocks.ListBlock(core_blocks.StructBlock((('number', core_blocks.CharBlock(help_text='Do not include spaces or dashes. Ex. 8554112372', max_length=15, validators=[django.core.validators.RegexValidator(message='Enter a numeric phone number, without punctuation.', regex='^\\d*$')])), ('extension', core_blocks.CharBlock(max_length=4, required=False)), ('vanity', core_blocks.CharBlock(help_text='A phoneword version of the above number. Include any formatting. Ex. (555) 222-CFPB', max_length=15, required=False)), ('tty', core_blocks.CharBlock(help_text='Do not include spaces or dashes. Ex. 8554112372', label='TTY', max_length=15, required=False, validators=[django.core.validators.RegexValidator(message='Enter a numeric phone number, without punctuation.', regex='^\\d*$')])), ('tty_ext', core_blocks.CharBlock(label='TTY Extension', max_length=4, required=False))))))))), ('address', core_blocks.StructBlock((('label', core_blocks.CharBlock(required=False)), ('title', core_blocks.CharBlock(required=False)), ('street', core_blocks.CharBlock(required=False)), ('city', core_blocks.CharBlock(max_length=50, required=False)), ('state', core_blocks.CharBlock(max_length=25, required=False)), ('zip_code', core_blocks.CharBlock(max_length=15, required=False)))))), blank=True))))), ('well', core_blocks.StructBlock((('content', core_blocks.RichTextBlock(label='Well', required=False)),))), ('video_player', core_blocks.StructBlock((('video_url', core_blocks.RegexBlock(default='https://www.youtube.com/embed/', error_messages={'invalid': 'The YouTube URL is in the wrong format. You must use the embed URL (https://www.youtube.com/embed/video_id), which can be obtained by clicking Share > Embed on the YouTube video page.', 'required': 'The YouTube URL field is required for video players.'}, label='YouTube Embed URL', regex='^https:\\/\\/www\\.youtube\\.com\\/embed\\/.+$', required=True)),))), ('snippet_list', core_blocks.StructBlock((('heading', core_blocks.CharBlock(required=False)), ('body', core_blocks.RichTextBlock(required=False)), ('has_top_rule_line', core_blocks.BooleanBlock(default=False, help_text='Check this to add a horizontal rule line above this block.', required=False)), ('image', core_blocks.StructBlock((('upload', images_blocks.ImageChooserBlock(required=False)), ('alt', core_blocks.CharBlock(help_text="If the image is decorative (i.e., if a screenreader wouldn't have anything useful to say about it), leave the Alt field blank.", required=False))))), ('actions_column_width', core_blocks.ChoiceBlock(choices=[('70', '70%'), ('66', '66%'), ('60', '60%'), ('50', '50%'), ('40', '40%'), ('33', '33%'), ('30', '30%')], help_text='Choose the width in % that you wish to set the Actions column in a resource list.', label='Width of "Actions" column', required=False)), ('show_thumbnails', core_blocks.BooleanBlock(help_text="If selected, each resource in the list will include a 150px-wide image from the resource's thumbnail field.", required=False)), ('actions', core_blocks.ListBlock(core_blocks.StructBlock((('link_label', core_blocks.CharBlock(help_text='E.g., "Download" or "Order free prints"')), ('snippet_field', core_blocks.ChoiceBlock(choices=[('related_file', 'Related file'), ('alternate_file', 'Alternate file'), ('link', 'Link'), ('alternate_link', 'Alternate link')], help_text='The field that the action link should point to')))))), ('tags', core_blocks.ListBlock(core_blocks.CharBlock(label='Tag'), help_text='Enter tag names to filter the snippets. For a snippet to match and be output in the list, it must have been tagged with all of the tag names listed here. The tag names are case-insensitive.'))))), ('table_block', v1.atomic_elements.organisms.AtomicTableBlock(table_options={'renderer': 'html'})), ('feedback', core_blocks.StructBlock((('was_it_helpful_text', core_blocks.CharBlock(default='Was this page helpful to you?', help_text='Use this field only for feedback forms that use "Was this helpful?" radio buttons.', required=False)), ('intro_text', core_blocks.CharBlock(help_text='Optional feedback intro', required=False)), ('question_text', core_blocks.CharBlock(help_text='Optional expansion on intro', required=False)), ('radio_intro', core_blocks.CharBlock(help_text='Leave blank unless you are building a feedback form with extra radio-button prompts, as in /owning-a-home/help-us-improve/.', required=False)), ('radio_text', core_blocks.CharBlock(default='This information helps us understand your question better.', required=False)), ('radio_question_1', core_blocks.CharBlock(default='How soon do you expect to buy a home?', required=False)), ('radio_question_2', core_blocks.CharBlock(default='Do you currently own a home?', required=False)), ('button_text', core_blocks.CharBlock(default='Submit')), ('contact_advisory', core_blocks.RichTextBlock(help_text='Use only for feedback forms that ask for a contact email', required=False))))), ('raw_html_block', core_blocks.RawHTMLBlock(label='Raw HTML block')), ('conference_registration_form', core_blocks.StructBlock((('govdelivery_code', core_blocks.CharBlock(help_text='Conference registrants will be subscribed to this GovDelivery topic.', label='GovDelivery code')), ('govdelivery_question_id', core_blocks.RegexBlock(error_messages={'invalid': 'GovDelivery question ID must be 5 digits.'}, help_text='Enter the ID of the question in GovDelivery that is being used to track registration for this conference. It is the number in the question URL, e.g., the <code>12345</code> in <code>https://admin.govdelivery.com/questions/12345/edit</code>.', label='GovDelivery question ID', regex='^\\d{5,}$', required=False)), ('govdelivery_answer_id', core_blocks.RegexBlock(error_messages={'invalid': 'GovDelivery answer ID must be 5 digits.'}, help_text='Enter the ID of the affirmative answer for the above question. To find it, right-click on the answer in the listing on a page like <code>https://admin.govdelivery.com/questions/12345/answers</code>, inspect the element, and look around in the source for a five-digit ID associated with that answer. <strong>Required if Govdelivery question ID is set.</strong>', label='GovDelivery answer ID', regex='^\\d{5,}$', required=False)), ('capacity', core_blocks.IntegerBlock(help_text='Enter the (physical) conference attendance limit as a number.')), ('success_message', core_blocks.RichTextBlock(help_text='Enter a message that will be shown on successful registration.')), ('at_capacity_message', core_blocks.RichTextBlock(help_text='Enter a message that will be shown when the event is at capacity.')), ('failure_message', core_blocks.RichTextBlock(help_text='Enter a message that will be shown if the GovDelivery subscription fails.'))))), ('chart_block', core_blocks.StructBlock((('title', core_blocks.CharBlock(required=True)), ('chart_type', core_blocks.ChoiceBlock(choices=[('bar', 'Bar | % y-axis values'), ('line', 'Line | millions/billions y-axis values'), ('line-index', 'Line-Index | integer y-axis values'), ('tile_map', 'Tile Map | grid-like USA map')])), ('color_scheme', core_blocks.ChoiceBlock(choices=[('blue', 'Blue'), ('gold', 'Gold'), ('green', 'Green'), ('navy', 'Navy'), ('neutral', 'Neutral'), ('purple', 'Purple'), ('teal', 'Teal')], help_text='Chart\'s color scheme. See "https://github.com/cfpb/cfpb-chart-builder#createchart-options-".', required=False)), ('data_source', core_blocks.CharBlock(help_text='Location of the chart\'s data source relative to "https://files.consumerfinance.gov/data/". For example,"consumer-credit-trends/auto-loans/num_data_AUT.csv".', required=True)), ('date_published', core_blocks.DateBlock(help_text='Automatically generated when CCT cron job runs')), ('description', core_blocks.CharBlock(help_text='Briefly summarize the chart for visually impaired users.', required=True)), ('has_top_rule_line', core_blocks.BooleanBlock(default=False, help_text='Check this to add a horizontal rule line to top of chart block.', required=False)), ('last_updated_projected_data', core_blocks.DateBlock(help_text='Month of latest entry in dataset')), ('metadata', core_blocks.CharBlock(help_text='Optional metadata for the chart to use. For example, with CCT this would be the chart\'s "group".', required=False)), ('note', core_blocks.CharBlock(help_text='Text to display as a footnote. For example, "Data from the last six months are not final."', required=False)), ('y_axis_label', core_blocks.CharBlock(help_text='Custom y-axis label. NOTE: Line-Index chart y-axis is not overridable with this field!', required=False))))), ('mortgage_chart_block', core_blocks.StructBlock((('content_block', core_blocks.RichTextBlock()), ('title', core_blocks.CharBlock(classname='title', required=True)), ('description', core_blocks.CharBlock(help_text='Chart summary for visually impaired users.', required=False)), ('note', core_blocks.CharBlock(help_text='Text for "Note" section of footnotes.', required=False)), ('has_top_rule_line', core_blocks.BooleanBlock(default=False, help_text='Check this to add a horizontal rule line to top of chart block.', required=False))))), ('mortgage_map_block', core_blocks.StructBlock((('content_block', core_blocks.RichTextBlock()), ('title', core_blocks.CharBlock(classname='title', required=True)), ('description', core_blocks.CharBlock(help_text='Chart summary for visually impaired users.', required=False)), ('note', core_blocks.CharBlock(help_text='Text for "Note" section of footnotes.', required=False)), ('has_top_rule_line', core_blocks.BooleanBlock(default=False, help_text='Check this to add a horizontal rule line to top of chart block.', required=False))))), ('mortgage_downloads_block', core_blocks.StructBlock((('show_archives', core_blocks.BooleanBlock(default=False, help_text='Check this box to allow the archival section to display. No section will appear if there are no archival downloads.', required=False)),))), ('data_snapshot', core_blocks.StructBlock((('market_key', core_blocks.CharBlock(help_text='Market identifier, e.g. AUT', max_length=20, required=True)), ('num_originations', core_blocks.CharBlock(help_text='Number of originations, e.g. 1.2 million', max_length=20)), ('value_originations', core_blocks.CharBlock(help_text='Total dollar value of originations, e.g. $3.4 billion', max_length=20)), ('year_over_year_change', core_blocks.CharBlock(help_text='Percentage change, e.g. 5.6% increase', max_length=20)), ('last_updated_projected_data', core_blocks.DateBlock(help_text='Month of latest entry in dataset')), ('num_originations_text', core_blocks.CharBlock(help_text='Descriptive sentence, e.g. Auto loans originated', max_length=100)), ('value_originations_text', core_blocks.CharBlock(help_text='Descriptive sentence, e.g. Dollar volume of new loans', max_length=100)), ('year_over_year_change_text', core_blocks.CharBlock(help_text='Descriptive sentence, e.g. In year-over-year originations', max_length=100)), ('inquiry_month', core_blocks.DateBlock(help_text='Month of latest entry in dataset for inquiry data', max_length=20, required=False)), ('inquiry_year_over_year_change', core_blocks.CharBlock(help_text='Percentage change, e.g. 5.6% increase', max_length=20, required=False)), ('inquiry_year_over_year_change_text', core_blocks.CharBlock(help_text='Descriptive sentence, e.g. In year-over-year inquiries', max_length=100, required=False)), ('tightness_month', core_blocks.DateBlock(help_text='Month of latest entry in dataset for credit tightness data', max_length=20, required=False)), ('tightness_year_over_year_change', core_blocks.CharBlock(help_text='Percentage change, e.g. 5.6% increase', max_length=20, required=False)), ('tightness_year_over_year_change_text', core_blocks.CharBlock(help_text='Descriptive sentence, e.g. In year-over-year credit tightness', max_length=100, required=False)), ('image', images_blocks.ImageChooserBlock(icon='image', required=False))))), ('job_listing_table', core_blocks.StructBlock((('first_row_is_table_header', core_blocks.BooleanBlock(default=True, help_text='Display the first row as a header.', required=False)), ('first_col_is_header', core_blocks.BooleanBlock(default=False, help_text='Display the first column as a header.', required=False)), ('is_full_width', core_blocks.BooleanBlock(default=False, help_text='Display the table at full width.', required=False)), ('is_striped', core_blocks.BooleanBlock(default=False, help_text='Display the table with striped rows.', required=False)), ('is_stacked', core_blocks.BooleanBlock(default=True, help_text='Stack the table columns on mobile.', required=False)), ('empty_table_msg', core_blocks.CharBlock(help_text='Message to display if there is no table data.', label='No Table Data Message', required=False)), ('hide_closed', core_blocks.BooleanBlock(default=True, help_text='Whether to hide jobs that are not currently open (jobs will automatically update)', required=False))))), ('bureau_structure', core_blocks.StructBlock((('last_updated_date', core_blocks.DateBlock(required=False)), ('download_image', docs_blocks.DocumentChooserBlock(icon='image', required=False)), ('director', core_blocks.CharBlock()), ('divisions', core_blocks.ListBlock(core_blocks.StructBlock((('name', core_blocks.CharBlock()), ('leads', core_blocks.ListBlock(core_blocks.StructBlock((('name', core_blocks.CharBlock()), ('title', core_blocks.TextBlock(required=False)))))), ('offices', core_blocks.ListBlock(core_blocks.StructBlock((('name', core_blocks.CharBlock()), ('leads', core_blocks.ListBlock(core_blocks.StructBlock((('name', core_blocks.CharBlock()), ('title', core_blocks.TextBlock(required=False)))))))))), ('overview_page', core_blocks.CharBlock()))))), ('office_of_the_director', core_blocks.ListBlock(core_blocks.StructBlock((('name', core_blocks.CharBlock()), ('leads', core_blocks.ListBlock(core_blocks.StructBlock((('name', core_blocks.CharBlock()), ('title', core_blocks.TextBlock(required=False)))))), ('offices', core_blocks.ListBlock(core_blocks.StructBlock((('name', core_blocks.CharBlock()), ('leads', core_blocks.ListBlock(core_blocks.StructBlock((('name', core_blocks.CharBlock()), ('title', core_blocks.TextBlock(required=False)))))))))))), label='Office of the Director'))))), ('yes_checklist', core_blocks.StructBlock((('checklist', core_blocks.ListBlock(core_blocks.StructBlock((('item', core_blocks.CharBlock(help_text='Short description for a checkbox item')), ('details', core_blocks.RichTextBlock(help_text='Deeper explanation of the item', required=False)))))),)))), blank=True),
        ),
        migrations.RunPython(migrate_forwards, migrate_backwards),
    ]
