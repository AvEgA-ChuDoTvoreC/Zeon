# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""

from apps.api.views import AddMeasurementsView, GetMeasurementsView
from apps.api import blueprint


blueprint.add_url_rule('/add_measurements', view_func=AddMeasurementsView.as_view('add_measurements'))
blueprint.add_url_rule('/get_measurements', view_func=GetMeasurementsView.as_view('get_measurements'))
