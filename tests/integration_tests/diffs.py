from .base import get_valid_item_type, create_geometry


def get_new_diff(item_type, diff_type=1, data=None):
    """
    1: Complete Activity with its Point somewhere in Laos.
    2: Incomplete Activity with its Point somewhere in Laos.
    3: Complete Activity with one or more Involvements (provided data array
       needed).
    4: Complete Activity with its Point somewhere in Laos and two values
       (IntegerDropdown) of Subcategory 8 filled out.
    """
    """
    1: Complete Stakeholder (minimal)
    2: Incomplete Stakeholder
    3: Complete Stakeholder with two values (IntegerDropdown) of Subcategory 8
       filled out.
    """
    item_type = get_valid_item_type(item_type)
    if item_type == 'a':
        if diff_type == 1:
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
        elif diff_type == 2:
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
        elif diff_type == 3:
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
        elif diff_type == 4:
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
        else:
            raise Exception('Invalid type for Activity diff: %s' % diff_type)
    else:
        if diff_type == 1:
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
        elif diff_type == 2:
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
        elif diff_type == 3:
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
            raise Exception(
                'Invalid type for Stakeholder diff: %s' % diff_type)


def get_edit_diff(item_type, uid, version=1, diff_type=1, data=None):
    """
    1: Add a new Taggroup to Activity (based on type 1 from getNewActivityDiff)
    2: Add or remove one or more existing Stakeholder (provided data array
       needed)
    3: Remove an existing Taggroup (based on type 1)
    """
    """
    1: Add a new Taggroup to Stakeholder (based on type 1 from
        getNewStakeholderDiff)
    """
    item_type = get_valid_item_type(item_type)
    if item_type == 'a':
        if diff_type == 1:
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
        elif diff_type == 2:
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
        elif diff_type == 3:
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
        elif diff_type == 4:
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
        elif diff_type == 5:
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
        else:
            raise Exception('Invalid type for Activity diff: %s' % diff_type)
    else:
        if diff_type == 1:
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
            raise Exception(
                'Invalid type for Stakeholder diff: %s' % diff_type)
