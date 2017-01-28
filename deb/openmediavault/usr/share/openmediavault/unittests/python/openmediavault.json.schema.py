# -*- coding: utf-8 -*-
#
# This file is part of OpenMediaVault.
#
# @license   http://www.gnu.org/licenses/gpl.html GPL Version 3
# @author    Volker Theile <volker.theile@openmediavault.org>
# @copyright Copyright (c) 2009-2017 Volker Theile
#
# OpenMediaVault is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# OpenMediaVault is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenMediaVault. If not, see <http://www.gnu.org/licenses/>.
import unittest
import openmediavault.json.schema

class SchemaTestCase(unittest.TestCase):
	def _get_schema(self):
		return openmediavault.json.Schema({
			"type": "object",
			"properties": {
				"name": { "type": "string", "required": True },
				"price": { "type": "number", "minimum": 35, "maximum": 40 }
			}
		})

	def test_get(self):
		schema = self._get_schema()
		schema.get()

	def test_get_by_path_success(self):
		schema = self._get_schema()
		schema.get_by_path("properties.price")

	def test_get_by_path_fail(self):
		schema = self._get_schema()
		self.assertRaises(openmediavault.json.SchemaPathException,
			lambda: schema.get_by_path("a.b.c"))

	def test_required(self):
		schema = self._get_schema()
		self.assertRaises(openmediavault.json.SchemaValidationException,
			lambda: schema.validate({ "price": 38 }))

	def test_validate_maximum(self):
		schema = self._get_schema()
		self.assertRaises(openmediavault.json.SchemaValidationException,
			lambda: schema.validate({ "name": "Apple", "price": 41 }))

	def test_validate_minimum(self):
		schema = self._get_schema()
		self.assertRaises(openmediavault.json.SchemaValidationException,
			lambda: schema.validate({ "name": "Eggs", "price": 34.99 }))

	def test_check_format_unknown(self):
		schema = openmediavault.json.Schema({})
		self.assertRaises(openmediavault.json.SchemaException, lambda:
			schema._check_format("abc", { "format": "abc" }, "abc"))

	def test_check_format_regex(self):
		schema = openmediavault.json.Schema({})
		schema._check_format('/^\d{4}-\d{2}-\d{2}$/',
			{ "format": "regex" }, "field1")

	def test_check_format_email(self):
		schema = openmediavault.json.Schema({})
		schema._check_format("test@test.com",
			{ "format": "email" }, "field2")

	def test_check_format_hostname(self):
		schema = openmediavault.json.Schema({})
		schema._check_format("myvault",
			{ "format": "host-name" }, "field3")

	def test_check_format_hostname_fail(self):
		schema = openmediavault.json.Schema({})
		self.assertRaises(openmediavault.json.SchemaValidationException,
			lambda: schema._check_format("myvault.local",
			{ "format": "host-name" }, "field3"))

	def test_check_one_of(self):
		schema = openmediavault.json.Schema({})
		schema._check_format("192.168.10.101", {
				"type": "string",
				"oneOf": [{
					"type": "string",
					"format": "ipv6"
				},{
					"type": "string",
					"format": "ipv4"
				}]
			}, "field3")

unittest.main()
