# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import xml.etree.ElementTree as ET

class Xml2PropertyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # read all line
        xml_str = self.view.substr(sublime.Region(0, self.view.size()))
        # xml to property
        property_str = self.xml_properties(xml_str)
        # open new window and insert
        w = self.view.window().new_file()
        w.insert(edit, 0, property_str)

    def xml_properties(self, xml_str):
        try:
            xml = ET.fromstring(xml_str)
        except Exception as e:
            sublime.status_message("xml format invalid!!")
            return        

        property_list = []
        for ele_property in xml.iter('property'):
            name = ''
            value = ''
            for inner_property in ele_property:
                if inner_property.tag == "name":
                    name = inner_property.text
                elif inner_property.tag == 'value':
                    value = inner_property.text

            property_list.append(name + '=' + value)

        return "\n".join(sorted(property_list))
