% for child in field:
    % if child.name == 'role_name':
        <div class="row-fluid">
            <h5 class="green">
                ${child.cstruct}
            </h5>
        </div>
    % elif child.name != 'role_id':
        <div class="row-fluid">
            ${child.render_template(field.widget.readonly_item_template)}
        </div>
    % endif
% endfor
<div class="row-fluid">
    <div class="offset5 span7">
        <a href="${request.route_url('stakeholders_read_one', output='html', uid=cstruct['id'])}">
            ${_('View Stakeholder')}
        </a>
    </div>
</div>
