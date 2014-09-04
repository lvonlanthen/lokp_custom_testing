/*

  *** IMPORTANT *** Use this script only to populate an *EMPTY* (after running
    lmkp_populate) database!

  This script will populate the following tables:
  - Categories
  - A_Keys
  - A_Values
  - SH_Keys
  - SH_Values
  - Profiles ('global', 'Laos', 'Peru', 'Madagascar', 'Cambodia')
  - Languages (add Code, Spanish to existing languages)
  - Stakeholder Roles
  - Institution Types
  - Users:
    - user1: active and approved, moderator in laos profile
    - user2: active and approved, regular user (in cambodia profile)
    - user3: active but not approved (in laos profile)
    - user4: inactive (in laos profile)

  It also links user 1 (addmin) with the global profile.

*/

INSERT INTO data.languages(id, english_name, local_name, locale) VALUES
    (2, 'Codes', 'Codes', 'code'),
    (3, 'Spanish', 'Español', 'es')
;
SELECT setval('data.languages_id_seq', 3, true);

INSERT INTO data.categories(id, name, type, fk_language, description, fk_category) VALUES
  (1, '[A] Category 1', 'activities', 1, NULL, NULL),
  (2, '[A] Category 2', 'activities', 1, NULL, NULL),
  (3, '[A] Category 3', 'activities', 1, NULL, NULL),
  (4, '[A] Subcategory 1', 'activities', 1, NULL, NULL),
  (5, '[A] Subcategory 2', 'activities', 1, NULL, NULL),
  (6, '[A] Subcategory 3', 'activities', 1, NULL, NULL),
  (7, '[A] Subcategory 4', 'activities', 1, NULL, NULL),
  (8, '[A] Subcategory 5', 'activities', 1, NULL, NULL),
  (9, '[A] Subcategory 6', 'activities', 1, NULL, NULL),
  (10, '[A] Subcategory 7', 'activities', 1, NULL, NULL),
  (11, '[A] Subcategory 8', 'activities', 1, NULL, NULL),
  (12, '[A] Subcategory 9', 'activities', 1, NULL, NULL),
  (13, '[A] Subcategory 10', 'activities', 1, NULL, NULL),
  (14, '[SH] Category 1', 'stakeholders', 1, NULL, NULL),
  (15, '[SH] Category 2', 'stakeholders', 1, NULL, NULL),
  (16, '[SH] Category 3', 'stakeholders', 1, NULL, NULL),
  (17, '[SH] Subcategory 1', 'stakeholders', 1, NULL, NULL),
  (18, '[SH] Subcategory 2', 'stakeholders', 1, NULL, NULL),
  (19, '[SH] Subcategory 3', 'stakeholders', 1, NULL, NULL),
  (20, '[SH] Subcategory 4', 'stakeholders', 1, NULL, NULL),
  (21, '[SH] Subcategory 5', 'stakeholders', 1, NULL, NULL),
  (22, '[SH] Subcategory 6', 'stakeholders', 1, NULL, NULL),
  (23, '[SH] Subcategory 7', 'stakeholders', 1, NULL, NULL),
  (24, '[SH] Subcategory 8', 'stakeholders', 1, NULL, NULL),
  (25, '[SH] Subcategory 9', 'stakeholders', 1, NULL, NULL),
  (26, '[SH] Subcategory 10', 'stakeholders', 1, NULL, NULL),
  (27, '[A-T] Category 1', NULL, 3, NULL, 1),
  (28, '[A-T] Category 2', NULL, 3, NULL, 2),
  (29, '[A-T] Category 3', NULL, 3, NULL, 3),
  (30, '[A-T] Subcategory 1', NULL, 3, NULL, 4),
  (31, '[A-T] Subcategory 2', NULL, 3, NULL, 5),
  (32, '[A-T] Subcategory 3', NULL, 3, NULL, 6),
  (33, '[A-T] Subcategory 4', NULL, 3, NULL, 7),
  (34, '[A-T] Subcategory 5', NULL, 3, NULL, 8),
  (35, '[A-T] Subcategory 6', NULL, 3, NULL, 9),
  (36, '[A-T] Subcategory 7', NULL, 3, NULL, 10),
  (37, '[A-T] Subcategory 8', NULL, 3, NULL, 11),
  (38, '[A-T] Subcategory 9', NULL, 3, NULL, 12),
  (39, '[A-T] Subcategory 10', NULL, 3, NULL, 13),
  (40, '[SH-T] Category 1', NULL, 3, NULL, 14),
  (41, '[SH-T] Category 2', NULL, 3, NULL, 15),
  (42, '[SH-T] Category 3', NULL, 3, NULL, 16),
  (43, '[SH-T] Subcategory 1', NULL, 3, NULL, 17),
  (44, '[SH-T] Subcategory 2', NULL, 3, NULL, 18),
  (45, '[SH-T] Subcategory 3', NULL, 3, NULL, 19),
  (46, '[SH-T] Subcategory 4', NULL, 3, NULL, 20),
  (47, '[SH-T] Subcategory 5', NULL, 3, NULL, 21),
  (48, '[SH-T] Subcategory 6', NULL, 3, NULL, 22),
  (49, '[SH-T] Subcategory 7', NULL, 3, NULL, 23),
  (50, '[SH-T] Subcategory 8', NULL, 3, NULL, 24),
  (51, '[SH-T] Subcategory 9', NULL, 3, NULL, 25),
  (52, '[SH-T] Subcategory 10', NULL, 3, NULL, 26),
  (53, '[A] Category 4', 'activities', 1, NULL, NULL),
  (54, '[A] Category 5', 'activities', 1, NULL, NULL),
  (55, '[SH] Category 4', 'stakeholders', 1, NULL, NULL),
  (56, '[SH] Category 5', 'stakeholders', 1, NULL, NULL)
;
SELECT setval('data.categories_id_seq', 56, true);

INSERT INTO data.a_keys(id, fk_a_key, fk_language, key, type, helptext, description, validator) VALUES
  (1, NULL, NULL, '[A] Textfield 1', 'String', NULL, NULL, NULL),
  (2, NULL, NULL, '[A] Textfield 2', 'String', NULL, NULL, NULL),
  (3, NULL, NULL, '[A] Textfield 3', 'String', NULL, NULL, NULL),
  (4, NULL, NULL, '[A] Textarea 1', 'Text', NULL, NULL, NULL),
  (5, NULL, NULL, '[A] Textarea 2', 'Text', NULL, NULL, NULL),
  (6, NULL, NULL, '[A] Textarea 3', 'Text', NULL, NULL, NULL),
  (7, NULL, NULL, '[A] Dropdown 1', 'Dropdown', NULL, NULL, NULL),
  (8, NULL, NULL, '[A] Dropdown 2', 'Dropdown', NULL, NULL, NULL),
  (9, NULL, NULL, '[A] Dropdown 3', 'Dropdown', NULL, NULL, NULL),
  (10, NULL, NULL, '[A] Checkbox 1', 'Checkbox', NULL, NULL, NULL),
  (11, NULL, NULL, '[A] Checkbox 2', 'Checkbox', NULL, NULL, NULL),
  (12, NULL, NULL, '[A] Checkbox 3', 'Checkbox', NULL, NULL, NULL),
  (13, NULL, NULL, '[A] Integerfield 1', 'Integer', NULL, NULL, NULL),
  (14, NULL, NULL, '[A] Integerfield 2', 'Integer', NULL, NULL, NULL),
  (15, NULL, NULL, '[A] Integerfield 3', 'Integer', NULL, NULL, NULL),
  (16, NULL, NULL, '[A] Numberfield 1', 'Number', NULL, NULL, NULL),
  (17, NULL, NULL, '[A] Numberfield 2', 'Number', NULL, NULL, NULL),
  (18, NULL, NULL, '[A] Numberfield 3', 'Number', NULL, NULL, NULL),
  (19, NULL, NULL, '[A] Datefield 1', 'Date', NULL, NULL, NULL),
  (20, NULL, NULL, '[A] Datefield 2', 'Date', NULL, NULL, NULL),
  (21, NULL, NULL, '[A] Datefield 3', 'Date', NULL, NULL, NULL),
  (22, NULL, NULL, '[A] Filefield 1', 'File', NULL, NULL, NULL),
  (23, NULL, NULL, '[A] Filefield 2', 'File', NULL, NULL, NULL),
  (24, NULL, NULL, '[A] Filefield 3', 'File', NULL, NULL, NULL),
  (25, NULL, NULL, '[A] Inputtoken 1', 'InputToken', NULL, NULL, NULL),
  (26, NULL, NULL, '[A] Inputtoken 2', 'InputToken', NULL, NULL, NULL),
  (27, NULL, NULL, '[A] Inputtoken 3', 'InputToken', NULL, NULL, NULL),
  (28, NULL, NULL, '[A] Integerdropdown 1', 'IntegerDropdown', NULL, NULL, '[1,5]'),
  (29, NULL, NULL, '[A] Integerdropdown 2', 'IntegerDropdown', NULL, NULL, '[1,5]'),
  (30, NULL, NULL, '[A] Integerdropdown 3', 'IntegerDropdown', NULL, NULL, '[1,5]'),
  (31, 1, 1, '[A] Textfield 1_', NULL, NULL, NULL, NULL),
  (32, 2, 1, '[A] Textfield 2', NULL, NULL, NULL, NULL),
  (33, 3, 1, '[A] Textfield 3', NULL, NULL, NULL, NULL),
  (34, 4, 1, '[A] Textarea 1', NULL, NULL, NULL, NULL),
  (35, 5, 1, '[A] Textarea 2', NULL, NULL, NULL, NULL),
  (36, 6, 1, '[A] Textarea 3', NULL, NULL, NULL, NULL),
  (37, 7, 1, '[A] Dropdown 1', NULL, NULL, NULL, NULL),
  (38, 8, 1, '[A] Dropdown 2', NULL, NULL, NULL, NULL),
  (39, 9, 1, '[A] Dropdown 3', NULL, NULL, NULL, NULL),
  (40, 10, 1, '[A] Checkbox 1', NULL, NULL, NULL, NULL),
  (41, 11, 1, '[A] Checkbox 2', NULL, NULL, NULL, NULL),
  (42, 12, 1, '[A] Checkbox 3', NULL, NULL, NULL, NULL),
  (43, 13, 1, '[A] Integerfield 1', NULL, NULL, NULL, NULL),
  (44, 14, 1, '[A] Integerfield 2', NULL, NULL, NULL, NULL),
  (45, 15, 1, '[A] Integerfield 3', NULL, NULL, NULL, NULL),
  (46, 16, 1, '[A] Numberfield 1', NULL, NULL, NULL, NULL),
  (47, 17, 1, '[A] Numberfield 2', NULL, NULL, NULL, NULL),
  (48, 18, 1, '[A] Numberfield 3', NULL, NULL, NULL, NULL),
  (49, 19, 1, '[A] Datefield 1', NULL, NULL, NULL, NULL),
  (50, 20, 1, '[A] Datefield 2', NULL, NULL, NULL, NULL),
  (51, 21, 1, '[A] Datefield 3', NULL, NULL, NULL, NULL),
  (52, 22, 1, '[A] Filefield 1', NULL, NULL, NULL, NULL),
  (53, 23, 1, '[A] Filefield 2', NULL, NULL, NULL, NULL),
  (54, 24, 1, '[A] Filefield 3', NULL, NULL, NULL, NULL),
  (55, 25, 1, '[A] Inputtoken 1', NULL, NULL, NULL, NULL),
  (56, 26, 1, '[A] Inputtoken 2', NULL, NULL, NULL, NULL),
  (57, 27, 1, '[A] Inputtoken 3', NULL, NULL, NULL, NULL),
  (58, 28, 1, '[A] Integerdropdown 1', NULL, NULL, NULL, NULL),
  (59, 29, 1, '[A] Integerdropdown 2', NULL, NULL, NULL, NULL),
  (60, 30, 1, '[A] Integerdropdown 3', NULL, NULL, NULL, NULL),
  (61, 1, 3, '[A-T] Identical Translation', NULL, NULL, NULL, NULL),
  (62, 2, 3, '[A-T] Textfield 2', NULL, NULL, NULL, NULL),
  (63, 3, 3, '[A-T] Identical Translation', NULL, NULL, NULL, NULL),
  (64, 4, 3, '[A-T] Textarea 1', NULL, NULL, NULL, NULL),
  (65, 5, 3, '[A-T] Textarea 2', NULL, NULL, NULL, NULL),
  (66, 6, 3, '[A-T] Textarea 3', NULL, NULL, NULL, NULL),
  (67, 7, 3, '[A-T] Dropdown 1', NULL, NULL, NULL, NULL),
  (68, 8, 3, '[A-T] Dropdown 2', NULL, NULL, NULL, NULL),
  (69, 9, 3, '[A-T] Dropdown 3', NULL, NULL, NULL, NULL),
  (70, 10, 3, '[A-T] Checkbox 1', NULL, NULL, NULL, NULL),
  (71, 11, 3, '[A-T] Checkbox 2', NULL, NULL, NULL, NULL),
  (72, 12, 3, '[A-T] Checkbox 3', NULL, NULL, NULL, NULL),
  (73, 13, 3, '[A-T] Integerfield 1', NULL, NULL, NULL, NULL),
  (74, 14, 3, '[A-T] Integerfield 2', NULL, NULL, NULL, NULL),
  (75, 15, 3, '[A-T] Integerfield 3', NULL, NULL, NULL, NULL),
  (76, 16, 3, '[A-T] Numberfield 1', NULL, NULL, NULL, NULL),
  (77, 17, 3, '[A-T] Numberfield 2', NULL, NULL, NULL, NULL),
  (78, 18, 3, '[A-T] Numberfield 3', NULL, NULL, NULL, NULL),
  (79, 19, 3, '[A-T] Datefield 1', NULL, NULL, NULL, NULL),
  (80, 20, 3, '[A-T] Datefield 2', NULL, NULL, NULL, NULL),
  (81, 21, 3, '[A-T] Datefield 3', NULL, NULL, NULL, NULL),
  (82, 22, 3, '[A-T] Filefield 1', NULL, NULL, NULL, NULL),
  (83, 23, 3, '[A-T] Filefield 2', NULL, NULL, NULL, NULL),
  (84, 24, 3, '[A-T] Filefield 3', NULL, NULL, NULL, NULL),
  (85, 25, 3, '[A-T] Inputtoken 1', NULL, NULL, NULL, NULL),
  (86, 26, 3, '[A-T] Inputtoken 2', NULL, NULL, NULL, NULL),
  (87, 27, 3, '[A-T] Inputtoken 3', NULL, NULL, NULL, NULL),
  (88, 28, 3, '[A-T] Integerdropdown 1', NULL, NULL, NULL, NULL),
  (89, 29, 3, '[A-T] Integerdropdown 2', NULL, NULL, NULL, NULL),
  (90, 30, 3, '[A-T] Integerdropdown 3', NULL, NULL, NULL, NULL)
;
SELECT setval('data.a_keys_id_seq', 90, true);

INSERT INTO data.a_values (id, fk_a_value, fk_language, value, fk_a_key, "order") VALUES
  (1, NULL, 1, '[A] Value A1', 7, NULL),
  (2, NULL, 1, '[A] Value A2', 7, NULL),
  (3, NULL, 1, '[A] Value A3', 7, NULL),
  (4, NULL, 1, '[A] Value A4', 7, NULL),
  (5, NULL, 1, '[A] Value A5', 7, NULL),
  (6, NULL, 1, '[A] Value B1', 8, NULL),
  (7, NULL, 1, '[A] Value B2', 8, NULL),
  (8, NULL, 1, '[A] Value B3', 8, NULL),
  (9, NULL, 1, '[A] Value B4', 8, NULL),
  (10, NULL, 1, '[A] Value B5', 8, NULL),
  (11, NULL, 1, '[A] Value B6', 8, NULL),
  (12, NULL, 1, '[A] Value B7', 8, NULL),
  (13, NULL, 1, '[A] Value B8', 8, NULL),
  (14, NULL, 1, '[A] Value B9', 8, NULL),
  (15, NULL, 1, '[A] Value B10', 8, NULL),
  (16, NULL, 1, '[A] Value B11', 8, NULL),
  (17, NULL, 1, '[A] Value B12', 8, NULL),
  (18, NULL, 1, '[A] Value B13', 8, NULL),
  (19, NULL, 1, '[A] Value B14', 8, NULL),
  (20, NULL, 1, '[A] Value B15', 8, NULL),
  (21, NULL, 1, '[A] Value B16', 8, NULL),
  (22, NULL, 1, '[A] Value B17', 8, NULL),
  (23, NULL, 1, '[A] Value B18', 8, NULL),
  (24, NULL, 1, '[A] Value B19', 8, NULL),
  (25, NULL, 1, '[A] Value B20', 8, NULL),
  (26, NULL, 1, '[A] Value C1', 9, NULL),
  (27, NULL, 1, '[A] Value C2', 9, NULL),
  (28, NULL, 1, '[A] Value C3', 9, NULL),
  (29, NULL, 1, '[A] Value D1', 10, NULL),
  (30, NULL, 1, '[A] Value D2', 10, NULL),
  (31, NULL, 1, '[A] Value D3', 10, NULL),
  (32, NULL, 1, '[A] Value D4', 10, NULL),
  (33, NULL, 1, '[A] Value D5', 10, NULL),
  (34, NULL, 1, '[A] Value E1', 11, NULL),
  (35, NULL, 1, '[A] Value E2', 11, NULL),
  (36, NULL, 1, '[A] Value E3', 11, NULL),
  (37, NULL, 1, '[A] Value E4', 11, NULL),
  (38, NULL, 1, '[A] Value E5', 11, NULL),
  (39, NULL, 1, '[A] Value E6', 11, NULL),
  (40, NULL, 1, '[A] Value E7', 11, NULL),
  (41, NULL, 1, '[A] Value E8', 11, NULL),
  (42, NULL, 1, '[A] Value E9', 11, NULL),
  (43, NULL, 1, '[A] Value E10', 11, NULL),
  (44, NULL, 1, '[A] Value E11', 11, NULL),
  (45, NULL, 1, '[A] Value E12', 11, NULL),
  (46, NULL, 1, '[A] Value E13', 11, NULL),
  (47, NULL, 1, '[A] Value E14', 11, NULL),
  (48, NULL, 1, '[A] Value E15', 11, NULL),
  (49, NULL, 1, '[A] Value E16', 11, NULL),
  (50, NULL, 1, '[A] Value E17', 11, NULL),
  (51, NULL, 1, '[A] Value E18', 11, NULL),
  (52, NULL, 1, '[A] Value E19', 11, NULL),
  (53, NULL, 1, '[A] Value E20', 11, NULL),
  (54, NULL, 1, '[A] Value F1', 12, NULL),
  (55, NULL, 1, '[A] Value F2', 12, NULL),
  (56, NULL, 1, '[A] Value F3', 12, NULL),
  (57, NULL, 1, '[A] Value G1', 25, NULL),
  (58, NULL, 1, '[A] Value G2', 25, NULL),
  (59, NULL, 1, '[A] Value G3', 25, NULL),
  (60, NULL, 1, '[A] Value G4', 25, NULL),
  (61, NULL, 1, '[A] Value G5', 25, NULL),
  (62, NULL, 1, '[A] Value H1', 26, NULL),
  (63, NULL, 1, '[A] Value H2', 26, NULL),
  (64, NULL, 1, '[A] Value H3', 26, NULL),
  (65, NULL, 1, '[A] Value H4', 26, NULL),
  (66, NULL, 1, '[A] Value H5', 26, NULL),
  (67, NULL, 1, '[A] Value H6', 26, NULL),
  (68, NULL, 1, '[A] Value H7', 26, NULL),
  (69, NULL, 1, '[A] Value H8', 26, NULL),
  (70, NULL, 1, '[A] Value H9', 26, NULL),
  (71, NULL, 1, '[A] Value H10', 26, NULL),
  (72, NULL, 1, '[A] Value H11', 26, NULL),
  (73, NULL, 1, '[A] Value H12', 26, NULL),
  (74, NULL, 1, '[A] Value H13', 26, NULL),
  (75, NULL, 1, '[A] Value H14', 26, NULL),
  (76, NULL, 1, '[A] Value H15', 26, NULL),
  (77, NULL, 1, '[A] Value H16', 26, NULL),
  (78, NULL, 1, '[A] Value H17', 26, NULL),
  (79, NULL, 1, '[A] Value H18', 26, NULL),
  (80, NULL, 1, '[A] Value H19', 26, NULL),
  (81, NULL, 1, '[A] Value H20', 26, NULL),
  (82, NULL, 1, '[A] Value I1', 27, NULL),
  (83, NULL, 1, '[A] Value I2', 27, NULL),
  (84, NULL, 1, '[A] Value I3', 27, NULL),
  (85, 1, 3, '[A-T] Value A1', NULL, NULL),
  (86, 2, 3, '[A-T] Value A2', NULL, NULL),
  (87, 3, 3, '[A-T] Value A3', NULL, NULL),
  (88, 4, 3, '[A-T] Value A4', NULL, NULL),
  (89, 5, 3, '[A-T] Value A5', NULL, NULL),
  (90, 6, 3, '[A-T] Value B1', NULL, NULL),
  (91, 7, 3, '[A-T] Value B2', NULL, NULL),
  (92, 8, 3, '[A-T] Value B3', NULL, NULL),
  (93, 9, 3, '[A-T] Value B4', NULL, NULL),
  (94, 10, 3, '[A-T] Value B5', NULL, NULL),
  (95, 11, 3, '[A-T] Value B6', NULL, NULL),
  (96, 12, 3, '[A-T] Value B7', NULL, NULL),
  (97, 13, 3, '[A-T] Value B8', NULL, NULL),
  (98, 14, 3, '[A-T] Value B9', NULL, NULL),
  (99, 15, 3, '[A-T] Value B10', NULL, NULL),
  (100, 16, 3, '[A-T] Value B11', NULL, NULL),
  (101, 17, 3, '[A-T] Value B12', NULL, NULL),
  (102, 18, 3, '[A-T] Value B13', NULL, NULL),
  (103, 19, 3, '[A-T] Value B14', NULL, NULL),
  (104, 20, 3, '[A-T] Value B15', NULL, NULL),
  (105, 21, 3, '[A-T] Value B16', NULL, NULL),
  (106, 22, 3, '[A-T] Value B17', NULL, NULL),
  (107, 23, 3, '[A-T] Value B18', NULL, NULL),
  (108, 24, 3, '[A-T] Value B19', NULL, NULL),
  (109, 25, 3, '[A-T] Value B20', NULL, NULL),
  (110, 26, 3, '[A-T] Value C1', NULL, NULL),
  (111, 27, 3, '[A-T] Value C2', NULL, NULL),
  (112, 28, 3, '[A-T] Value C3', NULL, NULL),
  (113, 29, 3, '[A-T] Value D1', NULL, NULL),
  (114, 30, 3, '[A-T] Value D2', NULL, NULL),
  (115, 31, 3, '[A-T] Value D3', NULL, NULL),
  (116, 32, 3, '[A-T] Value D4', NULL, NULL),
  (117, 33, 3, '[A-T] Value D5', NULL, NULL),
  (118, 34, 3, '[A-T] Value E1', NULL, NULL),
  (119, 35, 3, '[A-T] Value E2', NULL, NULL),
  (120, 36, 3, '[A-T] Value E3', NULL, NULL),
  (121, 37, 3, '[A-T] Value E4', NULL, NULL),
  (122, 38, 3, '[A-T] Value E5', NULL, NULL),
  (123, 39, 3, '[A-T] Value E6', NULL, NULL),
  (124, 40, 3, '[A-T] Value E7', NULL, NULL),
  (125, 41, 3, '[A-T] Value E8', NULL, NULL),
  (126, 42, 3, '[A-T] Value E9', NULL, NULL),
  (127, 43, 3, '[A-T] Value E10', NULL, NULL),
  (128, 44, 3, '[A-T] Value E11', NULL, NULL),
  (129, 45, 3, '[A-T] Value E12', NULL, NULL),
  (130, 46, 3, '[A-T] Value E13', NULL, NULL),
  (131, 47, 3, '[A-T] Value E14', NULL, NULL),
  (132, 48, 3, '[A-T] Value E15', NULL, NULL),
  (133, 49, 3, '[A-T] Value E16', NULL, NULL),
  (134, 50, 3, '[A-T] Value E17', NULL, NULL),
  (135, 51, 3, '[A-T] Value E18', NULL, NULL),
  (136, 52, 3, '[A-T] Value E19', NULL, NULL),
  (137, 53, 3, '[A-T] Value E20', NULL, NULL),
  (138, 54, 3, '[A-T] Value F1', NULL, NULL),
  (139, 55, 3, '[A-T] Value F2', NULL, NULL),
  (140, 56, 3, '[A-T] Value F3', NULL, NULL),
  (141, 57, 3, '[A-T] Value G1', NULL, NULL),
  (142, 58, 3, '[A-T] Value G2', NULL, NULL),
  (143, 59, 3, '[A-T] Value G3', NULL, NULL),
  (144, 60, 3, '[A-T] Value G4', NULL, NULL),
  (145, 61, 3, '[A-T] Value G5', NULL, NULL),
  (146, 62, 3, '[A-T] Value H1', NULL, NULL),
  (147, 63, 3, '[A-T] Value H2', NULL, NULL),
  (148, 64, 3, '[A-T] Value H3', NULL, NULL),
  (149, 65, 3, '[A-T] Value H4', NULL, NULL),
  (150, 66, 3, '[A-T] Value H5', NULL, NULL),
  (151, 67, 3, '[A-T] Value H6', NULL, NULL),
  (152, 68, 3, '[A-T] Value H7', NULL, NULL),
  (153, 69, 3, '[A-T] Value H8', NULL, NULL),
  (154, 70, 3, '[A-T] Value H9', NULL, NULL),
  (155, 71, 3, '[A-T] Value H10', NULL, NULL),
  (156, 72, 3, '[A-T] Value H11', NULL, NULL),
  (157, 73, 3, '[A-T] Value H12', NULL, NULL),
  (158, 74, 3, '[A-T] Value H13', NULL, NULL),
  (159, 75, 3, '[A-T] Value H14', NULL, NULL),
  (160, 76, 3, '[A-T] Value H15', NULL, NULL),
  (161, 77, 3, '[A-T] Value H16', NULL, NULL),
  (162, 78, 3, '[A-T] Value H17', NULL, NULL),
  (163, 79, 3, '[A-T] Value H18', NULL, NULL),
  (164, 80, 3, '[A-T] Value H19', NULL, NULL),
  (165, 81, 3, '[A-T] Value H20', NULL, NULL),
  (166, 82, 3, '[A-T] Value I1', NULL, NULL),
  (167, 83, 3, '[A-T] Value I2', NULL, NULL),
  (168, 84, 3, '[A-T] Value I3', NULL, NULL)
;
SELECT setval('data.a_values_id_seq', 168, true);

INSERT INTO data.sh_keys (id, fk_sh_key, fk_language, key, type, helptext, description, validator) VALUES
  (1, NULL, NULL, '[SH] Textfield 1', 'String', NULL, NULL, NULL),
  (2, NULL, NULL, '[SH] Textfield 2', 'String', NULL, NULL, NULL),
  (3, NULL, NULL, '[SH] Textfield 3', 'String', NULL, NULL, NULL),
  (4, NULL, NULL, '[SH] Textarea 1', 'Text', NULL, NULL, NULL),
  (5, NULL, NULL, '[SH] Textarea 2', 'Text', NULL, NULL, NULL),
  (6, NULL, NULL, '[SH] Textarea 3', 'Text', NULL, NULL, NULL),
  (7, NULL, NULL, '[SH] Dropdown 1', 'Dropdown', NULL, NULL, NULL),
  (8, NULL, NULL, '[SH] Dropdown 2', 'Dropdown', NULL, NULL, NULL),
  (9, NULL, NULL, '[SH] Dropdown 3', 'Dropdown', NULL, NULL, NULL),
  (10, NULL, NULL, '[SH] Checkbox 1', 'Checkbox', NULL, NULL, NULL),
  (11, NULL, NULL, '[SH] Checkbox 2', 'Checkbox', NULL, NULL, NULL),
  (12, NULL, NULL, '[SH] Checkbox 3', 'Checkbox', NULL, NULL, NULL),
  (13, NULL, NULL, '[SH] Integerfield 1', 'Integer', NULL, NULL, NULL),
  (14, NULL, NULL, '[SH] Integerfield 2', 'Integer', NULL, NULL, NULL),
  (15, NULL, NULL, '[SH] Integerfield 3', 'Integer', NULL, NULL, NULL),
  (16, NULL, NULL, '[SH] Numberfield 1', 'Number', NULL, NULL, NULL),
  (17, NULL, NULL, '[SH] Numberfield 2', 'Number', NULL, NULL, NULL),
  (18, NULL, NULL, '[SH] Numberfield 3', 'Number', NULL, NULL, NULL),
  (19, NULL, NULL, '[SH] Datefield 1', 'Date', NULL, NULL, NULL),
  (20, NULL, NULL, '[SH] Datefield 2', 'Date', NULL, NULL, NULL),
  (21, NULL, NULL, '[SH] Datefield 3', 'Date', NULL, NULL, NULL),
  (22, NULL, NULL, '[SH] Filefield 1', 'File', NULL, NULL, NULL),
  (23, NULL, NULL, '[SH] Filefield 2', 'File', NULL, NULL, NULL),
  (24, NULL, NULL, '[SH] Filefield 3', 'File', NULL, NULL, NULL),
  (25, NULL, NULL, '[SH] Inputtoken 1', 'InputToken', NULL, NULL, NULL),
  (26, NULL, NULL, '[SH] Inputtoken 2', 'InputToken', NULL, NULL, NULL),
  (27, NULL, NULL, '[SH] Inputtoken 3', 'InputToken', NULL, NULL, NULL),
  (28, NULL, NULL, '[SH] Integerdropdown 1', 'IntegerDropdown', NULL, NULL, '[1,5]'),
  (29, NULL, NULL, '[SH] Integerdropdown 2', 'IntegerDropdown', NULL, NULL, '[1,5]'),
  (30, NULL, NULL, '[SH] Integerdropdown 3', 'IntegerDropdown', NULL, NULL, '[1,5]'),
  (31, 1, 1, '[SH] Textfield 1', NULL, NULL, NULL, NULL),
  (32, 2, 1, '[SH] Textfield 2', NULL, NULL, NULL, NULL),
  (33, 3, 1, '[SH] Textfield 3', NULL, NULL, NULL, NULL),
  (34, 4, 1, '[SH] Textarea 1', NULL, NULL, NULL, NULL),
  (35, 5, 1, '[SH] Textarea 2', NULL, NULL, NULL, NULL),
  (36, 6, 1, '[SH] Textarea 3', NULL, NULL, NULL, NULL),
  (37, 7, 1, '[SH] Dropdown 1', NULL, NULL, NULL, NULL),
  (38, 8, 1, '[SH] Dropdown 2', NULL, NULL, NULL, NULL),
  (39, 9, 1, '[SH] Dropdown 3', NULL, NULL, NULL, NULL),
  (40, 10, 1, '[SH] Checkbox 1', NULL, NULL, NULL, NULL),
  (41, 11, 1, '[SH] Checkbox 2', NULL, NULL, NULL, NULL),
  (42, 12, 1, '[SH] Checkbox 3', NULL, NULL, NULL, NULL),
  (43, 13, 1, '[SH] Integerfield 1', NULL, NULL, NULL, NULL),
  (44, 14, 1, '[SH] Integerfield 2', NULL, NULL, NULL, NULL),
  (45, 15, 1, '[SH] Integerfield 3', NULL, NULL, NULL, NULL),
  (46, 16, 1, '[SH] Numberfield 1', NULL, NULL, NULL, NULL),
  (47, 17, 1, '[SH] Numberfield 2', NULL, NULL, NULL, NULL),
  (48, 18, 1, '[SH] Numberfield 3', NULL, NULL, NULL, NULL),
  (49, 19, 1, '[SH] Datefield 1', NULL, NULL, NULL, NULL),
  (50, 20, 1, '[SH] Datefield 2', NULL, NULL, NULL, NULL),
  (51, 21, 1, '[SH] Datefield 3', NULL, NULL, NULL, NULL),
  (52, 22, 1, '[SH] Filefield 1', NULL, NULL, NULL, NULL),
  (53, 23, 1, '[SH] Filefield 2', NULL, NULL, NULL, NULL),
  (54, 24, 1, '[SH] Filefield 3', NULL, NULL, NULL, NULL),
  (55, 25, 1, '[SH] Inputtoken 1', NULL, NULL, NULL, NULL),
  (56, 26, 1, '[SH] Inputtoken 2', NULL, NULL, NULL, NULL),
  (57, 27, 1, '[SH] Inputtoken 3', NULL, NULL, NULL, NULL),
  (58, 28, 1, '[SH] Integerdropdown 1', NULL, NULL, NULL, NULL),
  (59, 29, 1, '[SH] Integerdropdown 2', NULL, NULL, NULL, NULL),
  (60, 30, 1, '[SH] Integerdropdown 3', NULL, NULL, NULL, NULL),
  (61, 1, 3, '[SH-T] Identical Translation', NULL, NULL, NULL, NULL),
  (62, 2, 3, '[SH-T] Textfield 2', NULL, NULL, NULL, NULL),
  (63, 3, 3, '[SH-T] Identical Translation', NULL, NULL, NULL, NULL),
  (64, 4, 3, '[SH-T] Textarea 1', NULL, NULL, NULL, NULL),
  (65, 5, 3, '[SH-T] Textarea 2', NULL, NULL, NULL, NULL),
  (66, 6, 3, '[SH-T] Textarea 3', NULL, NULL, NULL, NULL),
  (67, 7, 3, '[SH-T] Dropdown 1', NULL, NULL, NULL, NULL),
  (68, 8, 3, '[SH-T] Dropdown 2', NULL, NULL, NULL, NULL),
  (69, 9, 3, '[SH-T] Dropdown 3', NULL, NULL, NULL, NULL),
  (70, 10, 3, '[SH-T] Checkbox 1', NULL, NULL, NULL, NULL),
  (71, 11, 3, '[SH-T] Checkbox 2', NULL, NULL, NULL, NULL),
  (72, 12, 3, '[SH-T] Checkbox 3', NULL, NULL, NULL, NULL),
  (73, 13, 3, '[SH-T] Integerfield 1', NULL, NULL, NULL, NULL),
  (74, 14, 3, '[SH-T] Integerfield 2', NULL, NULL, NULL, NULL),
  (75, 15, 3, '[SH-T] Integerfield 3', NULL, NULL, NULL, NULL),
  (76, 16, 3, '[SH-T] Numberfield 1', NULL, NULL, NULL, NULL),
  (77, 17, 3, '[SH-T] Numberfield 2', NULL, NULL, NULL, NULL),
  (78, 18, 3, '[SH-T] Numberfield 3', NULL, NULL, NULL, NULL),
  (79, 19, 3, '[SH-T] Datefield 1', NULL, NULL, NULL, NULL),
  (80, 20, 3, '[SH-T] Datefield 2', NULL, NULL, NULL, NULL),
  (81, 21, 3, '[SH-T] Datefield 3', NULL, NULL, NULL, NULL),
  (82, 22, 3, '[SH-T] Filefield 1', NULL, NULL, NULL, NULL),
  (83, 23, 3, '[SH-T] Filefield 2', NULL, NULL, NULL, NULL),
  (84, 24, 3, '[SH-T] Filefield 3', NULL, NULL, NULL, NULL),
  (85, 25, 3, '[SH-T] Inputtoken 1', NULL, NULL, NULL, NULL),
  (86, 26, 3, '[SH-T] Inputtoken 2', NULL, NULL, NULL, NULL),
  (87, 27, 3, '[SH-T] Inputtoken 3', NULL, NULL, NULL, NULL),
  (88, 28, 3, '[SH-T] Integerdropdown 1', NULL, NULL, NULL, NULL),
  (89, 29, 3, '[SH-T] Integerdropdown 2', NULL, NULL, NULL, NULL),
  (90, 30, 3, '[SH-T] Integerdropdown 3', NULL, NULL, NULL, NULL)
;
SELECT setval('data.sh_keys_id_seq', 90, true);

INSERT INTO data.sh_values (id, fk_sh_value, fk_language, value, fk_sh_key, "order") VALUES
  (1, NULL, 1, '[SH] Value A1', 7, NULL),
  (2, NULL, 1, '[SH] Value A2', 7, NULL),
  (3, NULL, 1, '[SH] Value A3', 7, NULL),
  (4, NULL, 1, '[SH] Value A4', 7, NULL),
  (5, NULL, 1, '[SH] Value A5', 7, NULL),
  (6, NULL, 1, '[SH] Value B1', 8, NULL),
  (7, NULL, 1, '[SH] Value B2', 8, NULL),
  (8, NULL, 1, '[SH] Value B3', 8, NULL),
  (9, NULL, 1, '[SH] Value B4', 8, NULL),
  (10, NULL, 1, '[SH] Value B5', 8, NULL),
  (11, NULL, 1, '[SH] Value B6', 8, NULL),
  (12, NULL, 1, '[SH] Value B7', 8, NULL),
  (13, NULL, 1, '[SH] Value B8', 8, NULL),
  (14, NULL, 1, '[SH] Value B9', 8, NULL),
  (15, NULL, 1, '[SH] Value B10', 8, NULL),
  (16, NULL, 1, '[SH] Value B11', 8, NULL),
  (17, NULL, 1, '[SH] Value B12', 8, NULL),
  (18, NULL, 1, '[SH] Value B13', 8, NULL),
  (19, NULL, 1, '[SH] Value B14', 8, NULL),
  (20, NULL, 1, '[SH] Value B15', 8, NULL),
  (21, NULL, 1, '[SH] Value B16', 8, NULL),
  (22, NULL, 1, '[SH] Value B17', 8, NULL),
  (23, NULL, 1, '[SH] Value B18', 8, NULL),
  (24, NULL, 1, '[SH] Value B19', 8, NULL),
  (25, NULL, 1, '[SH] Value B20', 8, NULL),
  (26, NULL, 1, '[SH] Value C1', 9, NULL),
  (27, NULL, 1, '[SH] Value C2', 9, NULL),
  (28, NULL, 1, '[SH] Value C3', 9, NULL),
  (29, NULL, 1, '[SH] Value D1', 10, NULL),
  (30, NULL, 1, '[SH] Value D2', 10, NULL),
  (31, NULL, 1, '[SH] Value D3', 10, NULL),
  (32, NULL, 1, '[SH] Value D4', 10, NULL),
  (33, NULL, 1, '[SH] Value D5', 10, NULL),
  (34, NULL, 1, '[SH] Value E1', 11, NULL),
  (35, NULL, 1, '[SH] Value E2', 11, NULL),
  (36, NULL, 1, '[SH] Value E3', 11, NULL),
  (37, NULL, 1, '[SH] Value E4', 11, NULL),
  (38, NULL, 1, '[SH] Value E5', 11, NULL),
  (39, NULL, 1, '[SH] Value E6', 11, NULL),
  (40, NULL, 1, '[SH] Value E7', 11, NULL),
  (41, NULL, 1, '[SH] Value E8', 11, NULL),
  (42, NULL, 1, '[SH] Value E9', 11, NULL),
  (43, NULL, 1, '[SH] Value E10', 11, NULL),
  (44, NULL, 1, '[SH] Value E11', 11, NULL),
  (45, NULL, 1, '[SH] Value E12', 11, NULL),
  (46, NULL, 1, '[SH] Value E13', 11, NULL),
  (47, NULL, 1, '[SH] Value E14', 11, NULL),
  (48, NULL, 1, '[SH] Value E15', 11, NULL),
  (49, NULL, 1, '[SH] Value E16', 11, NULL),
  (50, NULL, 1, '[SH] Value E17', 11, NULL),
  (51, NULL, 1, '[SH] Value E18', 11, NULL),
  (52, NULL, 1, '[SH] Value E19', 11, NULL),
  (53, NULL, 1, '[SH] Value E20', 11, NULL),
  (54, NULL, 1, '[SH] Value F1', 12, NULL),
  (55, NULL, 1, '[SH] Value F2', 12, NULL),
  (56, NULL, 1, '[SH] Value F3', 12, NULL),
  (57, NULL, 1, '[SH] Value G1', 25, NULL),
  (58, NULL, 1, '[SH] Value G2', 25, NULL),
  (59, NULL, 1, '[SH] Value G3', 25, NULL),
  (60, NULL, 1, '[SH] Value G4', 25, NULL),
  (61, NULL, 1, '[SH] Value G5', 25, NULL),
  (62, NULL, 1, '[SH] Value H1', 26, NULL),
  (63, NULL, 1, '[SH] Value H2', 26, NULL),
  (64, NULL, 1, '[SH] Value H3', 26, NULL),
  (65, NULL, 1, '[SH] Value H4', 26, NULL),
  (66, NULL, 1, '[SH] Value H5', 26, NULL),
  (67, NULL, 1, '[SH] Value H6', 26, NULL),
  (68, NULL, 1, '[SH] Value H7', 26, NULL),
  (69, NULL, 1, '[SH] Value H8', 26, NULL),
  (70, NULL, 1, '[SH] Value H9', 26, NULL),
  (71, NULL, 1, '[SH] Value H10', 26, NULL),
  (72, NULL, 1, '[SH] Value H11', 26, NULL),
  (73, NULL, 1, '[SH] Value H12', 26, NULL),
  (74, NULL, 1, '[SH] Value H13', 26, NULL),
  (75, NULL, 1, '[SH] Value H14', 26, NULL),
  (76, NULL, 1, '[SH] Value H15', 26, NULL),
  (77, NULL, 1, '[SH] Value H16', 26, NULL),
  (78, NULL, 1, '[SH] Value H17', 26, NULL),
  (79, NULL, 1, '[SH] Value H18', 26, NULL),
  (80, NULL, 1, '[SH] Value H19', 26, NULL),
  (81, NULL, 1, '[SH] Value H20', 26, NULL),
  (82, NULL, 1, '[SH] Value I1', 27, NULL),
  (83, NULL, 1, '[SH] Value I2', 27, NULL),
  (84, NULL, 1, '[SH] Value I3', 27, NULL),
  (85, 1, 3, '[SH-T] Value A1', NULL, NULL),
  (86, 2, 3, '[SH-T] Value A2', NULL, NULL),
  (87, 3, 3, '[SH-T] Value A3', NULL, NULL),
  (88, 4, 3, '[SH-T] Value A4', NULL, NULL),
  (89, 5, 3, '[SH-T] Value A5', NULL, NULL),
  (90, 6, 3, '[SH-T] Value B1', NULL, NULL),
  (91, 7, 3, '[SH-T] Value B2', NULL, NULL),
  (92, 8, 3, '[SH-T] Value B3', NULL, NULL),
  (93, 9, 3, '[SH-T] Value B4', NULL, NULL),
  (94, 10, 3, '[SH-T] Value B5', NULL, NULL),
  (95, 11, 3, '[SH-T] Value B6', NULL, NULL),
  (96, 12, 3, '[SH-T] Value B7', NULL, NULL),
  (97, 13, 3, '[SH-T] Value B8', NULL, NULL),
  (98, 14, 3, '[SH-T] Value B9', NULL, NULL),
  (99, 15, 3, '[SH-T] Value B10', NULL, NULL),
  (100, 16, 3, '[SH-T] Value B11', NULL, NULL),
  (101, 17, 3, '[SH-T] Value B12', NULL, NULL),
  (102, 18, 3, '[SH-T] Value B13', NULL, NULL),
  (103, 19, 3, '[SH-T] Value B14', NULL, NULL),
  (104, 20, 3, '[SH-T] Value B15', NULL, NULL),
  (105, 21, 3, '[SH-T] Value B16', NULL, NULL),
  (106, 22, 3, '[SH-T] Value B17', NULL, NULL),
  (107, 23, 3, '[SH-T] Value B18', NULL, NULL),
  (108, 24, 3, '[SH-T] Value B19', NULL, NULL),
  (109, 25, 3, '[SH-T] Value B20', NULL, NULL),
  (110, 26, 3, '[SH-T] Value C1', NULL, NULL),
  (111, 27, 3, '[SH-T] Value C2', NULL, NULL),
  (112, 28, 3, '[SH-T] Value C3', NULL, NULL),
  (113, 29, 3, '[SH-T] Value D1', NULL, NULL),
  (114, 30, 3, '[SH-T] Value D2', NULL, NULL),
  (115, 31, 3, '[SH-T] Value D3', NULL, NULL),
  (116, 32, 3, '[SH-T] Value D4', NULL, NULL),
  (117, 33, 3, '[SH-T] Value D5', NULL, NULL),
  (118, 34, 3, '[SH-T] Value E1', NULL, NULL),
  (119, 35, 3, '[SH-T] Value E2', NULL, NULL),
  (120, 36, 3, '[SH-T] Value E3', NULL, NULL),
  (121, 37, 3, '[SH-T] Value E4', NULL, NULL),
  (122, 38, 3, '[SH-T] Value E5', NULL, NULL),
  (123, 39, 3, '[SH-T] Value E6', NULL, NULL),
  (124, 40, 3, '[SH-T] Value E7', NULL, NULL),
  (125, 41, 3, '[SH-T] Value E8', NULL, NULL),
  (126, 42, 3, '[SH-T] Value E9', NULL, NULL),
  (127, 43, 3, '[SH-T] Value E10', NULL, NULL),
  (128, 44, 3, '[SH-T] Value E11', NULL, NULL),
  (129, 45, 3, '[SH-T] Value E12', NULL, NULL),
  (130, 46, 3, '[SH-T] Value E13', NULL, NULL),
  (131, 47, 3, '[SH-T] Value E14', NULL, NULL),
  (132, 48, 3, '[SH-T] Value E15', NULL, NULL),
  (133, 49, 3, '[SH-T] Value E16', NULL, NULL),
  (134, 50, 3, '[SH-T] Value E17', NULL, NULL),
  (135, 51, 3, '[SH-T] Value E18', NULL, NULL),
  (136, 52, 3, '[SH-T] Value E19', NULL, NULL),
  (137, 53, 3, '[SH-T] Value E20', NULL, NULL),
  (138, 54, 3, '[SH-T] Value F1', NULL, NULL),
  (139, 55, 3, '[SH-T] Value F2', NULL, NULL),
  (140, 56, 3, '[SH-T] Value F3', NULL, NULL),
  (141, 57, 3, '[SH-T] Value G1', NULL, NULL),
  (142, 58, 3, '[SH-T] Value G2', NULL, NULL),
  (143, 59, 3, '[SH-T] Value G3', NULL, NULL),
  (144, 60, 3, '[SH-T] Value G4', NULL, NULL),
  (145, 61, 3, '[SH-T] Value G5', NULL, NULL),
  (146, 62, 3, '[SH-T] Value H1', NULL, NULL),
  (147, 63, 3, '[SH-T] Value H2', NULL, NULL),
  (148, 64, 3, '[SH-T] Value H3', NULL, NULL),
  (149, 65, 3, '[SH-T] Value H4', NULL, NULL),
  (150, 66, 3, '[SH-T] Value H5', NULL, NULL),
  (151, 67, 3, '[SH-T] Value H6', NULL, NULL),
  (152, 68, 3, '[SH-T] Value H7', NULL, NULL),
  (153, 69, 3, '[SH-T] Value H8', NULL, NULL),
  (154, 70, 3, '[SH-T] Value H9', NULL, NULL),
  (155, 71, 3, '[SH-T] Value H10', NULL, NULL),
  (156, 72, 3, '[SH-T] Value H11', NULL, NULL),
  (157, 73, 3, '[SH-T] Value H12', NULL, NULL),
  (158, 74, 3, '[SH-T] Value H13', NULL, NULL),
  (159, 75, 3, '[SH-T] Value H14', NULL, NULL),
  (160, 76, 3, '[SH-T] Value H15', NULL, NULL),
  (161, 77, 3, '[SH-T] Value H16', NULL, NULL),
  (162, 78, 3, '[SH-T] Value H17', NULL, NULL),
  (163, 79, 3, '[SH-T] Value H18', NULL, NULL),
  (164, 80, 3, '[SH-T] Value H19', NULL, NULL),
  (165, 81, 3, '[SH-T] Value H20', NULL, NULL),
  (166, 82, 3, '[SH-T] Value I1', NULL, NULL),
  (167, 83, 3, '[SH-T] Value I2', NULL, NULL),
  (168, 84, 3, '[SH-T] Value I3', NULL, NULL)
;
SELECT setval('data.sh_values_id_seq', 168, true);

INSERT INTO data.profiles (id, code, polygon) VALUES (1, 'global', '0103000020E6100000010000000500000000000000008066C000000000000055C0000000000080664000000000000055C00000000000806640000000000000554000000000008066C0000000000000554000000000008066C000000000000055C0');
INSERT INTO data.profiles (id, code, polygon) VALUES (2, 'laos', '0103000020E6100000010000000500000077BE9F1A2F055940C442AD69DED12B40713D0AD7A3E85A40C442AD69DED12B40713D0AD7A3E85A40FCA9F1D24D82364077BE9F1A2F055940FCA9F1D24D82364077BE9F1A2F055940C442AD69DED12B40');
INSERT INTO data.profiles (id, code, polygon) VALUES (3, 'peru', '0103000020E610000001000000050000008C31B08EE35454C0295C8FC2F55832C0AE47E17A142A51C0295C8FC2F55832C0AE47E17A142A51C0B81E85EB51B89EBF8C31B08EE35454C0B81E85EB51B89EBF8C31B08EE35454C0295C8FC2F55832C0');
INSERT INTO data.profiles (id, code, polygon) VALUES (4, 'madagascar', '0103000020E610000001000000050000001F85EB51B89E45406666666666E627C000000000004049406666666666E627C00000000000404940D7A3703D0A9739C01F85EB51B89E4540D7A3703D0A9739C01F85EB51B89E45406666666666E627C0');
INSERT INTO data.profiles (id, code, polygon) VALUES (5, 'cambodia', '0103000020E6100000010000001E000000FEFFFFBFBFB9594098000040C6D323400A0000C05FB959401000002045D42340FEFFFF3F6EB859401801006029DA23400E00008049B85940180000001ADD23400A0000C076965940900000003B8D2A40020000003396594070000060FAB02A400E0000C88795594060000030F0122B400A000060929559403800004015162B40060000E0A89559405800008093182B4006000080F0955940880000C0881D2B40120000803DBC5940900000A0D1622C402AE66D2432BD5940A0E026CC7D692C400E000020CFC35940780000C0FF902C40060000D029C95940A00000101DA62C400A000020C5CA5940380000C009AA2C400A000080CEE35940180000C019D82C40020000A02AE5594020000060BAD92C40FEFFFFBF4EEA59400000000085DF2C40363333136BE25A40F0999939C0602D40FEFFFF7F80E35A40100000A0945F2D4006000080AEE35A4078000050FC5D2D40060000C051E85A40580000A0B1B82A4002000000C2E55A4060000020CF1D29400E0000E001E55A401000002055FA28400A0000A081E35A401000008050C2284046984E19F8E25A406095868B2DB6284002000060C1E25A4018000080D7B228405E555595298C5A40C0555575ED932540120000C0C9BB59402000000083D42340FEFFFFBFBFB9594098000040C6D32340');
SELECT setval('data.profiles_id_seq', 5, true);

INSERT INTO data.users(id, uuid, username, email, firstname, lastname, privacy, registration_timestamp, is_active, activation_uuid, is_approved, fk_institution, password) VALUES
  (2, '032f1ef8-8db9-41e9-b18d-170da6ea288e', 'user1', 'lukas.vonlanthen@cde.unibe.ch', '', '', 1, '2014-07-21 09:30:00.000+02', true, NULL, true, NULL, '$p5k2$1000$W_xPYQFaism2IVAdnx-Oyg==$JSA4ab8fFYNc8jzDMz-TkszzxO4='),
  (3, 'ebf77c29-267a-43d0-a85d-4c1fe8a4b196', 'user2', 'lukas.vonlanthen@cde.unibe.ch', '', '', 1, '2014-07-21 09:30:00.000+02', true, NULL, true, NULL, '$p5k2$1000$W_xPYQFaism2IVAdnx-Oyg==$JSA4ab8fFYNc8jzDMz-TkszzxO4='),
  (4, '9d124316-d853-41f0-a9c2-dd177d649113', 'user3', 'lukas.vonlanthen@cde.unibe.ch', '', '', 1, '2014-07-21 09:30:00.000+02', true, NULL, false, NULL, '$p5k2$1000$W_xPYQFaism2IVAdnx-Oyg==$JSA4ab8fFYNc8jzDMz-TkszzxO4='),
  (5, 'c48f2afc-a642-4571-b469-01a7416dc355', 'user4', 'lukas.vonlanthen@cde.unibe.ch', '', '', 1, '2014-07-21 09:30:00.000+02', false, 'ff0f0050-bf5e-4361-954b-4b95809d6e32', false, NULL, '$p5k2$1000$W_xPYQFaism2IVAdnx-Oyg==$JSA4ab8fFYNc8jzDMz-TkszzxO4=')
;
SELECT setval('data.users_id_seq', 5, true);

INSERT INTO data.users_profiles(id, fk_user, fk_profile) VALUES
  (1, 1, 1),
  (2, 2, 2),
  (3, 3, 3),
  (4, 4, 2),
  (5, 5, 2)
;
SELECT setval('data.users_profiles_id_seq', 5, true);

INSERT INTO data.users_groups(id, fk_user, fk_group) VALUES
  (5, 2, 2),
  (6, 2, 3),
  (7, 3, 3),
  (8, 4, 3),
  (9, 5, 3)
;
SELECT setval('data.users_groups_id_seq', 9, true);

INSERT INTO data.stakeholder_roles(id, name, description) VALUES
  (1, 'Stakeholder Role 1', NULL),
  (2, 'Stakeholder Role 2', NULL),
  (3, 'Stakeholder Role 3', NULL),
  (4, 'Stakeholder Role 4', NULL),
  (5, 'Stakeholder Role 5', NULL),
  (6, 'Stakeholder Role 6', NULL),
  (7, 'Stakeholder Role 7', NULL),
  (8, 'Stakeholder Role 8', NULL),
  (9, 'Stakeholder Role 9', NULL),
  (10, 'Stakeholder Role 10', NULL)
;
SELECT setval('data.stakeholder_roles_id_seq', 10, true);

INSERT INTO data.institution_types(id, name, description) VALUES
    (1, 'CSO', NULL),
    (2, 'Government', NULL)
;
SELECT setval('data.institution_types_id_seq', 2, true);
