## Form to CREATE or EDIT an activity.

<%
    import colander
    new_form = 'id' not in cstruct or cstruct['id'] == colander.null
    _ = request.translate
%>

<h3>${_('Deal Editor')}</h3>

% if new_form is True:
    <p class="id">${_('New Deal')}</p>
% else:
    <p class="id">${cstruct['id']}</p>
% endif

<form
    id="${field.formid}"
    action="${field.action}"
    method="${field.method}"
    enctype="multipart/form-data"
    accept-charset="utf-8">

    <input type="hidden"
           name="_charset_"
    />
    <input type="hidden"
           name="__formid__"
           value="${field.formid}"
    />

    % if field.error:
        <div class="row-fluid">
            <div class="span9">
                <div class="alert alert-error">
                    <h5>${request.translate("There was a problem with your submission")}</h5>
                    ${request.translate("Errors have been highlighted below")}
                </div>
            </div>
        </div>
    % endif

    <div class="deal-editor-menu-bar">
        % for button in field.buttons:
            <ul>
                % if button.css_class == 'formstepactive':
                    <div class="active-wrapper">
                % endif

                <li
                    % if button.name == 'submit':
                        style="background-color:gray;"
                    % elif button.name == 'delete':
                        class="form-button-delete"
                    % endif
                    >
                    <button
                        id="${field.formid + button.name}"
                        name="${button.name}"
                        value="${button.value}"
                        class="btnText ${button.css_class}">
                        ${button.title}
                    </button>
                    % if button.css_class == 'formstepvisited':
                        <span class="form-button-visited"><i class="icon-ok-sign"></i></span>
                    % endif
                </li>

                % if button.css_class == 'formstepactive':
                    </div>
                % endif
            </ul>
        % endfor
        <div class="delete-confirm alert alert-error hide">
            <p>${_('Are you sure you want to delete this Activity?')}</p>
            <button name="delete" class="btn btn-danger">${_('Delete')}</button>
            <button id="delete-confirm-cancel" class="btn">${_('Cancel')}</button>
        </div>
    </div>

    % for child in field.children:
        ${child.render_template(field.widget.item_template)}
    % endfor

% if field.use_ajax:
    <script type="text/javascript">
        deform.addCallback(
            '${field.formid}',
            function(oid) {
                var target = '#' + oid;
                var options = {
                    target: target,
                    replaceTarget: true,
                    success: function() {
                        deform.processCallbacks();
                        deform.focusFirstInput(target);
                    }
               };
               var extra_options = ${field.ajax_options} || {};
               $('#' + oid).ajaxForm($.extend(options, extra_options));
            }
        );
    </script>
% endif

</form>
