from RRHH.serializers import CompanySerializer


def jwt_response_payload_handler(token, company=None, request=None):
    return {
        'token': token,
        'company': CompanySerializer(company, context={'request': request}).data
    }
