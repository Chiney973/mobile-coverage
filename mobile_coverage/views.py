from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions

from mobile_coverage.handlers import (
    get_geo_point_from_address,
    get_closest_coverage_for_each_provider_from_point
)

from mobile_coverage import AddressNotFound


class MobileCoverageView(APIView):

    def get(self, request):
        address = request.query_params.get("q")
        if not address:
            return Response()
        try:
            point = get_geo_point_from_address(address)
        except AddressNotFound:
            raise exceptions.ParseError(detail="address not found")
        providers_coverage = get_closest_coverage_for_each_provider_from_point(point)
        return Response(providers_coverage)
