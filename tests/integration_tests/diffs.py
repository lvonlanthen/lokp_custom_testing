#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import create_geometry


def get_new_diff(diff_type, data=[]):
    """
    Returns changeset diff which can be used to create a new Activity or
    a Stakeholder.

    Args:
        diff_type (int): The type of the diff to return. The following
            types are possible:
            101: [A] A complete Activity with its Point somewhere in
                Laos.
            102: [A] An incomplete Activity with its Point somewhere in
                Laos.
            103: [A] A complete Activity with one or more Involvements
                and its Point somewhere in Laos.
                (provided data array needed)
            104: [A] A complete Activity with two values
                (IntegerDropdown) of Subcategory 8 filled out and its
                Point somewhere in Laos.
            105: [A] A complete Activity with special characters and
                its Point somewhere in Laos.
            106: [A] A complete Activity with different attributes, one
                or more involvements and its Point somewhere in Laos.
                (provided data array needed)
            107: [A] A complete Activity with a repeating taggroups and
                its Point somewhere in Laos.
            108: [A] A complete Activity with two textfields (where
                translation is identical) filled out and its Point
                somewhere in Laos.
            109: [A] A complete Activity with a (simulated) file upload
                and its Point somewhere in Laos.
            110: [A] A complete Activity with its Point somewhere in
                Laos.
            111: [A] A complete Activity with its Point somewhere in
                Laos.
            201: [SH] A complete Stakeholder.
            202: [SH] An incomplete Stakeholder.
            203: [SH] A complete Stakeholder with two values
                (IntegerDropdown) of Subcategory 8 filled out.
            204: [SH] A complete Stakeholder with special characters.
            205: [SH] A complete Stakeholder with different attributes.
            206: [SH] A complete Stakeholder with repeating taggroups.
            207: [SH] A complete Stakeholder with a (simulated) file
                upload
            208: [SH] A complete Stakeholder with two textfields (where
                translation is identical) filled out.

    Kwargs:
        data (list): Additional data needed to create the diff.

    Returns:
        dict. The changeset diff.

    Raises:
        Exception
    """
    if diff_type == 101:
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value A1',
                                'key': u'[A] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value A1',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 123.45,
                                'key': u'[A] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.45,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 102:
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value D2',
                                'key': u'[A] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value D2',
                                    'key': u'[A] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': u'[A] Value D3',
                                'key': u'[A] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value D3',
                                    'key': u'[A] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 103:
        involvements = []
        for d in data:
            op = 'add' if 'op' not in d else d['op']
            involvements.append({
                'id': d['id'],
                'version': d['version'],
                'role': d['role'],
                'op': op
            })
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value A1',
                                'key': u'[A] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value A1',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 123.45,
                                'key': u'[A] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.45,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1,
                    'stakeholders': involvements
                }
            ]
        }
    elif diff_type == 104:
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value A2',
                                'key': u'[A] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value A2',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 123.45,
                                'key': u'[A] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.45,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'key': '[A] Integerdropdown 1',
                                'value': 1
                            },
                            'tags': [
                                {
                                    'key': '[A] Integerdropdown 1',
                                    'value': 1,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'key': '[A] Integerdropdown 2',
                                'value': 2
                            },
                            'tags': [
                                {
                                    'key': '[A] Integerdropdown 2',
                                    'value': 2,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 105:
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value A1',
                                'key': u'[A] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value A1',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }, {
                                    'key': '[A] Textarea 1',
                                    'value': "Foo ‰öäüñ Æò' dróżką ສອບ",
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 123.45,
                                'key': u'[A] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.45,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 106:
        involvements = []
        for d in data:
            op = 'add' if 'op' not in d else d['op']
            involvements.append({
                'id': d['id'],
                'version': d['version'],
                'role': d['role'],
                'op': op
            })
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value A1',
                                'key': u'[A] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value A1',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }, {
                                    'key': '[A] Textarea 1',
                                    'value': "Foo ‰öäüñ Æò' dróżką ສອບ",
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '[A] Value D2',
                                'key': u'[A] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': '[A] Value D2',
                                    'key': u'[A] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '[A] Value D3',
                                'key': u'[A] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': '[A] Value D3',
                                    'key': u'[A] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 'This is Textfield 1',
                                'key': u'[A] Textfield 1'
                            },
                            'tags': [
                                {
                                    'value': 'This is Textfield 1',
                                    'key': u'[A] Textfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 1.23,
                                'key': u'[A] Numberfield 2'
                            },
                            'tags': [
                                {
                                    'value': 1.23,
                                    'key': u'[A] Numberfield 2',
                                    'op': 'add'
                                }, {
                                    'key': '[A] Integerfield 1',
                                    'value': 159,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 2.34,
                                'key': u'[A] Numberfield 2'
                            },
                            'tags': [
                                {
                                    'value': 2.34,
                                    'key': u'[A] Numberfield 2',
                                    'op': 'add'
                                }, {
                                    'key': '[A] Integerfield 1',
                                    'value': 123,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 123.45,
                                'key': u'[A] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.45,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '[A] Value B11',
                                'key': u'[A] Dropdown 2'
                            },
                            'tags': [
                                {
                                    'value': '[A] Value B11',
                                    'key': u'[A] Dropdown 2',
                                    'op': 'add'
                                }, {
                                    'value': '2014-08-05',
                                    'key': u'[A] Datefield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'key': '[A] Integerdropdown 1',
                                'value': 1
                            },
                            'tags': [
                                {
                                    'key': '[A] Integerdropdown 1',
                                    'value': 1,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'key': '[A] Integerdropdown 2',
                                'value': 2
                            },
                            'tags': [
                                {
                                    'key': '[A] Integerdropdown 2',
                                    'value': 2,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1,
                    'stakeholders': involvements
                }
            ]
        }
    elif diff_type == 107:
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value A1',
                                'key': u'[A] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value A1',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 1.23,
                                'key': u'[A] Numberfield 2'
                            },
                            'tags': [
                                {
                                    'value': 1.23,
                                    'key': u'[A] Numberfield 2',
                                    'op': 'add'
                                }, {
                                    'key': '[A] Integerfield 1',
                                    'value': 159,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 2.34,
                                'key': u'[A] Numberfield 2'
                            },
                            'tags': [
                                {
                                    'value': 2.34,
                                    'key': u'[A] Numberfield 2',
                                    'op': 'add'
                                }, {
                                    'key': '[A] Integerfield 1',
                                    'value': 123,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 123.45,
                                'key': u'[A] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.45,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 108:
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value A1',
                                'key': u'[A] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value A1',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 'First remark',
                                'key': u'[A] Textfield 1'
                            },
                            'tags': [
                                {
                                    'value': 'First remark',
                                    'key': u'[A] Textfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 'Second remark',
                                'key': u'[A] Textfield 3'
                            },
                            'tags': [
                                {
                                    'value': 'Second remark',
                                    'key': u'[A] Textfield 3',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 123.45,
                                'key': u'[A] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.45,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    if diff_type == 109:
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value A1',
                                'key': u'[A] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value A1',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 123.45,
                                'key': u'[A] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.45,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '[A] Value B1',
                                'key': u'[A] Dropdown 2'
                            },
                            'tags': [
                                {
                                    'value': '[A] Value B1',
                                    'key': u'[A] Dropdown 2',
                                    'op': 'add'
                                }, {
                                    'key': '[A] Filefield 1',
                                    'value': 'filename1.jpg|891f3b35-29d3-4ef2'
                                    '-93d4-2ca45ff718ea,filename2.pdf|56256744'
                                    '-cf88-434f-90b7-25db9f0fb0a0',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 110:
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value A3',
                                'key': u'[A] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value A3',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 99,
                                'key': u'[A] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 99,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 111:
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[A] Value A2',
                                'key': u'[A] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': u'[A] Value A2',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 1000000,
                                'key': u'[A] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 1000000,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 201:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': 123.0,
                                'key': u'[SH] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.0,
                                    'key': u'[SH] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': u'asdf',
                                'key': u'[SH] Textfield 1'
                            },
                            'tags': [
                                {
                                    'value': u'asdf',
                                    'key': u'[SH] Textfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 202:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': '[SH] Value D2',
                                'key': u'[SH] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': '[SH] Value D2',
                                    'key': u'[SH] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '[SH] Value D5',
                                'key': u'[SH] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': '[SH] Value D5',
                                    'key': u'[SH] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 203:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': 123.0,
                                'key': u'[SH] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.0,
                                    'key': u'[SH] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': u'asdf',
                                'key': u'[SH] Textfield 1'
                            },
                            'tags': [
                                {
                                    'value': u'asdf',
                                    'key': u'[SH] Textfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 1,
                                'key': '[SH] Integerdropdown 1'
                            },
                            'tags': [
                                {
                                    'value': 1,
                                    'key': '[SH] Integerdropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 2,
                                'key': '[SH] Integerdropdown 2'
                            },
                            'tags': [
                                {
                                    'value': 2,
                                    'key': '[SH] Integerdropdown 2',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 204:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': 123.0,
                                'key': u'[SH] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.0,
                                    'key': u'[SH] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 'Foo ‰öäüñ Æò" dróżką ສອບ',
                                'key': u'[SH] Textfield 1'
                            },
                            'tags': [
                                {
                                    'value': 'Foo ‰öäüñ Æò" dróżką ສອບ',
                                    'key': u'[SH] Textfield 1',
                                    'op': 'add'
                                }, {
                                    'value': 'Foo text',
                                    'key': '[SH] Textarea 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 205:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': 123.0,
                                'key': u'[SH] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.0,
                                    'key': u'[SH] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 'Foo ‰öäüñ Æò" dróżką ສອບ',
                                'key': u'[SH] Textfield 1'
                            },
                            'tags': [
                                {
                                    'value': 'Foo ‰öäüñ Æò" dróżką ສອບ',
                                    'key': u'[SH] Textfield 1',
                                    'op': 'add'
                                }, {
                                    'value': 'Foo text',
                                    'key': '[SH] Textarea 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '[SH] Value D2',
                                'key': u'[SH] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': '[SH] Value D2',
                                    'key': u'[SH] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '[SH] Value D3',
                                'key': u'[SH] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': '[SH] Value D3',
                                    'key': u'[SH] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '[SH] Value A1',
                                'key': u'[SH] Dropdown 1'
                            },
                            'tags': [
                                {
                                    'value': '[SH] Value A1',
                                    'key': u'[SH] Dropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 1.23,
                                'key': u'[SH] Numberfield 2'
                            },
                            'tags': [
                                {
                                    'value': 1.23,
                                    'key': u'[SH] Numberfield 2',
                                    'op': 'add'
                                }, {
                                    'key': '[SH] Integerfield 1',
                                    'value': 159,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 2.34,
                                'key': u'[SH] Numberfield 2'
                            },
                            'tags': [
                                {
                                    'value': 2.34,
                                    'key': u'[SH] Numberfield 2',
                                    'op': 'add'
                                }, {
                                    'key': '[SH] Integerfield 1',
                                    'value': 123,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '[SH] Value B11',
                                'key': u'[SH] Dropdown 2'
                            },
                            'tags': [
                                {
                                    'value': '[SH] Value B11',
                                    'key': u'[SH] Dropdown 2',
                                    'op': 'add'
                                }, {
                                    'value': '2014-08-05',
                                    'key': u'[SH] Datefield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 206:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': 123.0,
                                'key': u'[SH] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.0,
                                    'key': u'[SH] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 'Foo ‰öäüñ Æò" dróżką ສອບ',
                                'key': u'[SH] Textfield 1'
                            },
                            'tags': [
                                {
                                    'value': 'Foo ‰öäüñ Æò" dróżką ສອບ',
                                    'key': u'[SH] Textfield 1',
                                    'op': 'add'
                                }, {
                                    'value': 'Foo text',
                                    'key': '[SH] Textarea 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 1.23,
                                'key': u'[SH] Numberfield 2'
                            },
                            'tags': [
                                {
                                    'value': 1.23,
                                    'key': u'[SH] Numberfield 2',
                                    'op': 'add'
                                }, {
                                    'key': '[SH] Integerfield 1',
                                    'value': 159,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 2.34,
                                'key': u'[SH] Numberfield 2'
                            },
                            'tags': [
                                {
                                    'value': 2.34,
                                    'key': u'[SH] Numberfield 2',
                                    'op': 'add'
                                }, {
                                    'key': '[SH] Integerfield 1',
                                    'value': 123,
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 207:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': 123.0,
                                'key': u'[SH] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.0,
                                    'key': u'[SH] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': u'asdf',
                                'key': u'[SH] Textfield 1'
                            },
                            'tags': [
                                {
                                    'value': u'asdf',
                                    'key': u'[SH] Textfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '[SH] Value B1',
                                'key': u'[SH] Dropdown 2'
                            },
                            'tags': [
                                {
                                    'value': '[SH] Value B1',
                                    'key': u'[SH] Dropdown 2',
                                    'op': 'add'
                                }, {
                                    'key': '[SH] Filefield 1',
                                    'value': 'filename1.jpg|891f3b35-29d3-4ef2'
                                    '-93d4-2ca45ff718ea,filename2.pdf|56256744'
                                    '-cf88-434f-90b7-25db9f0fb0a0',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    elif diff_type == 208:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': 123.0,
                                'key': u'[SH] Numberfield 1'
                            },
                            'tags': [
                                {
                                    'value': 123.0,
                                    'key': u'[SH] Numberfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': u'First Remark',
                                'key': u'[SH] Textfield 1'
                            },
                            'tags': [
                                {
                                    'value': u'First Remark',
                                    'key': u'[SH] Textfield 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': u'Second Remark',
                                'key': u'[SH] Textfield 3'
                            },
                            'tags': [
                                {
                                    'value': u'Second Remark',
                                    'key': u'[SH] Textfield 3',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': 1
                }
            ]
        }
    else:
        raise Exception('Invalid item_type: %s' % diff_type)


def get_edit_diff(diff_type, uid, version=1, data=[]):
    """
    Returns changeset diff which can be used to edit an Activity or a
    Stakeholder.

    Args:
        diff_type (int): The type of the diff to return. The following
            types are possible:
            101: [A] Add a new Taggroup to an Activity.
                (based on type 101 from get_new_diff)
            102: [A] Add or remove one or more existing Stakeholder.
                (provided data array needed)
            103: [A] Remove an existing Taggroup.
                (based on type 101 from get_new_diff)
            104: [A] Edit the MainTag of an existing Taggroup.
                (based on type 101 from get_new_diff)
            105: [A] Add a Tag to an existing Taggroup.
                (based on type 101 from get_new_diff)
            106: [A] Edit the geometry of an Activity.
            107: [A] Edit a Tag (not the MainTag) of an existing
                Taggroup.
                (based on type 105 from get_new_diff)
            108: [A] Remove a Tag from an existing Taggroup
                (based on type 105 from get_new_diff)
            109: [A] Different attribute and involvement operations
                (based on type 106 from get_new_diff, data array needed)
            110: [A] Delete an Activity, optionally with involvements
                (based on type 101 from get_new_diff)
            201: [SH] Add a new Taggroup to a Stakeholder.
                (based on type 201 from get_new_diff)
            202: [SH] Remove an existing Taggroup.
                (based on type 201 from get_new_diff)
            203: [SH] Edit the MainTag of an existing Taggroup.
                (based on type 204 from get_new_diff)
            204: [SH] Edit a Tag of an existing Taggroup.
                (based on type 204 from get_new_diff)
            205: [SH] Add a Tag to an existing Taggroup.
                (based on type 201 from get_new_diff)
            206: [SH] Remove a Tag from an existing Taggroup
                (based on type 204 from get_new_diff)
            207: [SH] Different attribute operations
                (based on type 205 from get_new_diff)
            208: [SH] Delete a Stakeholder
                (based on type 201 from get_new_diff)
        uid (str): The identifier of the Activity or Stakeholder.

    Kwargs:
        version (int): The version the changeset will be applied to.
            Default: 1
        data (list): Additional data needed to create the diff.

    Returns:
        dict. The changeset diff.

    Raises:
        Exception
    """
    if diff_type == 101:
        return {
            'activities': [
                {
                    'taggroups': [
                        {
                            'main_tag': {
                                'key': '[A] Checkbox 1',
                                'value': '[A] Value D1'
                            },
                            'tags': [
                                {
                                    'key': '[A] Checkbox 1',
                                    'value': '[A] Value D1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 102:
        involvements = []
        for d in data:
            op = 'add' if 'op' not in d else d['op']
            involvements.append({
                'id': d['id'],
                'version': d['version'],
                'role': d['role'],
                'op': op
            })
        return {
            'activities': [
                {
                    'stakeholders': involvements,
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 103:
        return {
            'activities': [
                {
                    'taggroups': [
                        {
                            'tg_id': 1,
                            'tags': [
                                {
                                    'value': u'[A] Value A1',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'delete'
                                }
                            ],
                            'op': 'delete'
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 104:
        return {
            'activities': [
                {
                    'taggroups': [
                        {
                            'tg_id': 1,
                            'tags': [
                                {
                                    'value': u'[A] Value A1',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'delete'
                                }, {
                                    'value': u'[A] Value A2',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'add'
                                }
                            ]
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 105:
        return {
            'activities': [
                {
                    'taggroups': [
                        {
                            'tg_id': 1,
                            'tags': [
                                {
                                    'value': u'Foo Text',
                                    'key': u'[A] Textarea 1',
                                    'op': 'add'
                                }
                            ]
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 106:
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 107:
        return {
            'activities': [
                {
                    'taggroups': [
                        {
                            'tg_id': 1,
                            'tags': [
                                {
                                    'key': '[A] Textarea 1',
                                    'value': "Foo ‰öäüñ Æò' dróżką ສອບ",
                                    'op': 'delete'
                                }, {
                                    'key': u'[A] Textarea 1',
                                    'value': u'Bar ç"ö',
                                    'op': 'add'
                                }
                            ]
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 108:
        return {
            'activities': [
                {
                    'taggroups': [
                        {
                            'tg_id': 1,
                            'tags': [
                                {
                                    'key': '[A] Textarea 1',
                                    'value': "Foo ‰öäüñ Æò' dróżką ສອບ",
                                    'op': 'delete'
                                }
                            ]
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 109:
        involvements = []
        for d in data:
            op = 'add' if 'op' not in d else d['op']
            involvements.append({
                'id': d['id'],
                'version': d['version'],
                'role': d['role'],
                'op': op
            })
        return {
            'activities': [
                {
                    'geometry': create_geometry('laos'),
                    'taggroups': [
                        {
                            'tg_id': 1,
                            'tags': [
                                {
                                    'key': '[A] Textarea 1',
                                    'value': "Foo ‰öäüñ Æò' dróżką ສອບ",
                                    'op': 'delete'
                                }
                            ]
                        }, {
                            'tg_id': 2,
                            'tags': [
                                {
                                    'value': '[A] Value D2',
                                    'key': u'[A] Checkbox 1',
                                    'op': 'delete'
                                }
                            ],
                            'op': 'delete'
                        }, {
                            'main_tag': {
                                'value': '[A] Value D4',
                                'key': u'[A] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': '[A] Value D4',
                                    'key': u'[A] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': 'This is Textfield 2',
                                'key': u'[A] Textfield 2'
                            },
                            'tags': [
                                {
                                    'value': 'This is Textfield 2',
                                    'key': u'[A] Textfield 2',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'stakeholders': involvements,
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 110:
        involvements = []
        for d in data:
            op = 'add' if 'op' not in d else d['op']
            involvements.append({
                'id': d['id'],
                'version': d['version'],
                'role': d['role'],
                'op': op
            })
        diff = {
            'activities': [
                {
                    'taggroups': [
                        {
                            'tg_id': 1,
                            'tags': [
                                {
                                    'value': u'[A] Value A1',
                                    'key': u'[A] Dropdown 1',
                                    'op': 'delete'
                                }
                            ],
                            'op': 'delete'
                        }, {
                            'tg_id': 2,
                            'tags': [
                                {
                                    'value': 123.45,
                                    'key': u'[A] Numberfield 1',
                                    'op': 'delete'
                                }
                            ],
                            'op': 'delete'
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
        if len(involvements) > 0:
            diff['activities'][0]['stakeholders'] = involvements
        return diff
    elif diff_type == 201:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'main_tag': {
                                'value': u'[SH] Value D1',
                                'key': u'[SH] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': u'[SH] Value D1',
                                    'key': u'[SH] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 202:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'tg_id': 2,
                            'tags': [
                                {
                                    'value': 'asdf',
                                    'key': '[SH] Textfield 1',
                                    'op': 'delete'
                                }
                            ],
                            'op': 'delete'
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 203:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'tg_id': 2,
                            'tags': [
                                {
                                    'value': 'Foo ‰öäüñ Æò" dróżką ສອບ',
                                    'key': u'[SH] Textfield 1',
                                    'op': 'delete'
                                }, {
                                    'value': 'Bar %&ä£',
                                    'key': u'[SH] Textfield 1',
                                    'op': 'add'
                                }
                            ]
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 204:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'tg_id': 2,
                            'tags': [
                                {
                                    'value': 'Foo text',
                                    'key': '[SH] Textarea 1',
                                    'op': 'delete'
                                }, {
                                    'value': 'Bar text',
                                    'key': '[SH] Textarea 1',
                                    'op': 'add'
                                }
                            ]
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 205:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'tg_id': 2,
                            'tags': [
                                {
                                    'value': 'Foo',
                                    'key': '[SH] Textarea 1',
                                    'op': 'add'
                                }
                            ]
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 206:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'tg_id': 2,
                            'tags': [
                                {
                                    'value': 'Foo text',
                                    'key': '[SH] Textarea 1',
                                    'op': 'delete'
                                }
                            ]
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 207:
        return {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'tg_id': 2,
                            'tags': [
                                {
                                    'key': '[SH] Textarea 1',
                                    'value': "Foo ‰öäüñ Æò' dróżką ສອບ",
                                    'op': 'delete'
                                }
                            ]
                        }, {
                            'tg_id': 3,
                            'tags': [
                                {
                                    'value': '[SH] Value D2',
                                    'key': u'[SH] Checkbox 1',
                                    'op': 'delete'
                                }
                            ],
                            'op': 'delete'
                        }, {
                            'main_tag': {
                                'value': '[SH] Value D4',
                                'key': u'[SH] Checkbox 1'
                            },
                            'tags': [
                                {
                                    'value': '[SH] Value D4',
                                    'key': u'[SH] Checkbox 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }, {
                            'main_tag': {
                                'value': '1',
                                'key': u'[SH] Integerdropdown 1'
                            },
                            'tags': [
                                {
                                    'value': '1',
                                    'key': u'[SH] Integerdropdown 1',
                                    'op': 'add'
                                }
                            ],
                            'op': 'add'
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
    elif diff_type == 208:
        involvements = []
        for d in data:
            op = 'add' if 'op' not in d else d['op']
            involvements.append({
                'id': d['id'],
                'version': d['version'],
                'role': d['role'],
                'op': op
            })
        diff = {
            'stakeholders': [
                {
                    'taggroups': [
                        {
                            'tg_id': 1,
                            'tags': [
                                {
                                    'value': 123.0,
                                    'key': u'[SH] Numberfield 1',
                                    'op': 'delete'
                                }
                            ],
                            'op': 'delete'
                        }, {
                            'tg_id': 2,
                            'tags': [
                                {
                                    'value': u'asdf',
                                    'key': u'[SH] Textfield 1',
                                    'op': 'delete'
                                }
                            ],
                            'op': 'delete'
                        }
                    ],
                    'version': version,
                    'id': uid
                }
            ]
        }
        if len(involvements) > 0:
            diff['stakeholders'][0]['activities'] = involvements
        return diff
    else:
        raise Exception('Invalid diff_type: %s' % diff_type)
