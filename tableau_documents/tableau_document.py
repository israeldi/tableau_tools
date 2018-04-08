# -*- coding: utf-8 -*-

from ..tableau_base import TableauBase
from ..tableau_exceptions import *

# This class is just a shell so that TableauWorkbook and TableauDatasource can look the same from TableauFile
# This is probably not that Pythonic but whatevs
class TableauDocument(TableauBase):
    def __init__(self):
        TableauBase.__init__(self)
        self._datasources = []
        self._document_type = None
        self.parameters = None

    @property
    def datasources(self):
        """
        :rtype: list[TableauDatasource]
        """
        return self._datasources

    @property
    def document_type(self):
        """
        :rtype: unicode
        """
        return self._document_type

    def save_file(self, filename_no_extension, save_to_directory=None):
        """
        :type filename_no_extension: unicode
        :type save_to_directory: unicode
        :rtype: bool
        """
        return True


class TableauColumns(TableauBase):
    def __init__(self, columns_list, logger_obj=None):
        self.logger = logger_obj
        self.log_debug(u'Initializing a TableauColumns object')
        self.__translation_dict = None
        # List of lxml columns objects
        self.columns_list = columns_list

    def set_translation_dict(self, trans_dict):
        self.start_log_block()
        self.__translation_dict = trans_dict
        self.end_log_block()

    def translate_captions(self):
        self.start_log_block()
        for column in self.columns_list:
            if column.getroot().get('caption') is None:
                trans = self.__find_translation(column.getroot().get('name'))
            else:
                # Try to match caption first, if not move to name
                trans = self.__find_translation(column.getroot().get('caption'))
                if trans is None:
                    trans = self.__find_translation(column.getroot().get('name'))
            if trans is not None:
                column.getroot().set('caption', trans)
        self.end_log_block()

    def __find_translation(self, match_str):
        self.start_log_block()
        d = self.__translation_dict.get(match_str)
        self.end_log_block()
        return d


class TableauColumn(TableauBase):
    def __init__(self, column_xml_obj, logger_obj=None):
        """
        :type column_xml_obj: etree.Element
        :param logger_obj:
        """
        self.logger = logger_obj
        self.log_debug(u'Initializing TableauColumn object')
        self.xml_obj = column_xml_obj

    @property
    def alias(self):
        return self.xml_obj.get(u'caption')

    @alias.setter
    def alias(self, alias):
        """
        :type alias: unicode
        :return:
        """
        self.xml_obj.set(u'caption', alias)

    @property
    def datatype(self):
        return self.xml_obj.get(u'datatype')

    @alias.setter
    def datatype(self, datatype):
        """
        :type datatype: unicode
        :return:
        """
        if datatype.lower() not in [u'string', u'integer', u'datetime', u'date', u'real', u'boolean']:
            raise InvalidOptionException(u"{} is not a valid datatype".format(datatype))
        self.xml_obj.set(u'datatype', datatype)

    @property
    def column_name(self):
        return self.xml_obj.get(u'name')

    @column_name.setter
    def column_name(self, column_name):
        """
        :type column_name: unicode
        :return:
        """
        if column_name[0] == u"[" and column_name[-1] == u"]":
            new_column_name = column_name
        else:
            new_column_name = u"[{}]".format(column_name)
        self.xml_obj.set(u'name', new_column_name)

    @property
    def dimension_or_measure(self):
        return self.xml_obj.get(u'role')

    @dimension_or_measure.setter
    def dimension_or_measure(self, dimension_or_measure):
        """
        :type dimension_or_measure: unicode
        :return:
        """
        final_dimension_or_measure = dimension_or_measure.lower()
        if final_dimension_or_measure not in [u'dimension', u'measure']:
            raise InvalidOptionException(u'dimension_or_measure must be "dimension" or "measure"')
        self.xml_obj.set(u'role', final_dimension_or_measure)

    @property
    def aggregation_type(self):
        return self.xml_obj.get(u'type')

    @aggregation_type.setter
    def aggregation_type(self, aggregation_type):
        """
        :type aggregation_type: unicode
        :return:
        """
        final_aggregation_type = aggregation_type.lower()
        if final_aggregation_type not in [u'ordinal', u'nominal', u'quantitative']:
            raise InvalidOptionException(u'aggregation_type must be "ordinal", "nominal" or "quantiative"')
        self.xml_obj.set(u'type', final_aggregation_type)


class TableauHierarchies(TableauBase):
    def __init__(self, hierarchies_xml, logger_obj=None):
        self.logger = logger_obj
        self.log_debug(u'Initializing TableauHierarchies object')
        self.xml_obj = hierarchies_xml
        self.hierarchies = self.xml_obj.findall(u'./drill-path')


