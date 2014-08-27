from .base import create_geometry


def get_new_diff(diff_type, data=None):
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
            201: [SH] A complete Stakeholder.
            202: [SH] An incomplete Stakeholder.
            203: [SH] A complete Stakeholder with two values
                (IntegerDropdown) of Subcategory 8 filled out.

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
    else:
        raise Exception('Invalid item_type: %s' % diff_type)


def get_edit_diff(diff_type, uid, version=1, data=None):
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
            104: [A] Edit a Tag inside an existing Taggroup.
                (based on type 101 from get_new_diff)
            105: [A] Add a Tag to an existing Taggroup.
                (based on type 101 from get_new_diff)
            106: [A] Edit the geometry of an Activity.
            201: [SH] Add a new Taggroup to a Stakeholder.
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
    else:
        raise Exception('Invalid diff_type: %s' % diff_type)
