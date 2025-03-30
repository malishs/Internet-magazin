from rest_framework.metadata import BaseMetadata

class CustomMetadata(BaseMetadata):
    """
    Класс, который определяет метаданные для API.
    """
    def determine_metadata(self, request, view):
        # Возвращаем имя и описание
        return {
            "name": view.get_view_name(),
            "description": view.get_view_description(),
            "allowed_methods": view.allowed_methods,
            "renders": view.renderer_classes,
            "parses": view.parser_classes,
        }