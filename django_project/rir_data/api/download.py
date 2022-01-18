import os
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill
from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rir_data.models.instance import Instance
from rir_data.models.indicator.indicator_value import IndicatorValue

from openpyxl.workbook import Workbook
from django.conf import settings


class DownloadMasterData(APIView):
    """
    Download master data as spreadsheet
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, slug, date):
        instance = get_object_or_404(
            Instance, slug=slug
        )
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponseBadRequest('Date format is not correct')
        today_date = datetime.today().date().strftime("%Y-%m-%d")

        folder = os.path.join(
            settings.MEDIA_ROOT, 'download-data', request.user.username, today_date)
        if not os.path.exists(folder):
            os.makedirs(folder)
        _file = os.path.join(folder, date.strftime("%Y-%m-%d") + '.xlsx')

        # ----------------------------------------------
        # ----------------- SAVING DATA ----------------
        # ----------------------------------------------
        wb = Workbook()
        del wb['Sheet']
        instance_insicators = instance.indicators
        geometries = instance.geometries()
        for instance_level in instance.geometry_instance_levels:
            # check the indicators
            indicators = instance_insicators.filter(
                geometry_reporting_level=instance_level.level).order_by('name')
            if not indicators:
                continue

            # create new sheet
            sheet = wb.create_sheet(instance_level.level.name)
            row = 0

            def insert_sheet(row, column, value, color=None):
                sheet.cell(row=row + 1, column=column + 1).value = value
                if color:
                    sheet.cell(row=row + 1, column=column + 1).fill = PatternFill(
                        "solid", fgColor=color.replace('#', ''))

            # create headers
            header = [f'{instance_level.level.name} Name', f'{instance_level.level.name} Code']
            for idx, indicator in enumerate(indicators):
                header.append(indicator.name)
                header.append(f'{indicator.name} value')

            # safe header to excel
            for idx, _header in enumerate(header):
                insert_sheet(row, idx, _header)

            # get lines per geometry
            for geometry in geometries.filter(
                    geometry_level=instance_level.level):
                values = IndicatorValue.objects.filter(
                    indicator__in=indicators, geometry=geometry
                ).filter(date=date)
                if not values:
                    continue

                line = [''] * len(header)
                line[0] = geometry.name
                line[1] = geometry.identifier

                colors = [''] * len(header)
                for value in values:
                    indicator = value.indicator
                    indicator_text = header.index(indicator.name)
                    indicator_value = header.index(f'{indicator.name} value')
                    rule = indicator.scenario_rule_by_value(value.value)
                    line[indicator_value] = value.value
                    if rule:
                        color = rule.color if rule.color else rule.scenario_level.background_color
                        line[indicator_text] = rule.name if rule else ''
                        colors[indicator_value] = color
                        colors[indicator_text] = color

                row += 1
                for idx, _line in enumerate(line):
                    insert_sheet(row, idx, _line, colors[idx])

            # resize column
            for i, column_width in enumerate(header, 1):
                sheet.column_dimensions[get_column_letter(i)].width = 20

        # save output reports to excel file
        wb.save(filename=_file)
        # ----------------------------------------------

        if os.path.exists(_file):
            with open(_file, "rb") as excel:
                data = excel.read()

            response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={date.strftime("%Y-%m-%d")}_Master_Data.xlsx'
            os.remove(_file)
            return response
        else:
            return HttpResponseNotFound('The file is not found')
