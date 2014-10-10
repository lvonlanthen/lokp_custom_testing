<%
    isStakeholder = 'itemType' in cstruct and cstruct['itemType'] == 'stakeholders'
    statusId = cstruct['statusId'] if 'statusId' in cstruct else '2'
    empty = cstruct['taggroup_count'] == '0'

    from pyramid.security import ACLAllowed
    from pyramid.security import has_permission
    isModerator = isinstance(has_permission('moderate', request.context, request), ACLAllowed)

    if isStakeholder:
        routeName = 'stakeholders_read_one'
        historyRouteName = 'stakeholders_read_one_history'
        editLinkText = _('Edit this Investor')
        deleteLinkText = _('Delete this Stakeholder')
        deleteConfirmText = _('Are you sure you want to delete this Stakeholder?')
        form_id = 'stakeholderform'
    else:
        routeName = 'activities_read_one'
        historyRouteName = 'activities_read_one_history'
        editLinkText = _('Edit this Deal')
        deleteLinkText = _('Delete this Activity')
        deleteConfirmText = _('Are you sure you want to delete this Activity?')
        form_id = 'activityform'
%>

% if statusId != '2':
    <div class="row-fluid">
        <div class="span12 alert alert-block">
            % if statusId == '1':
                ## Pending
                <h4>${_('Pending Version')}</h4>
                <p>${_('You are seeing a pending version which needs to be reviewed before it is publicly visible.')}</p>
            % elif statusId == '3':
                ## Inactive
                <h4>${_('Inactive Version')}</h4>
                <p>${_('You are seeing an inactive version which is not active anymore.')}</p>
            % else:
                ## All the rest (deleted, rejected, edited).
                ## TODO: Should there be a separate messages for these statuses?
                <h4>${_('Not an active Version')}</h4>
                <p>${_('You are seeing a version which is not active.')}</p>
            % endif
        </div>
    </div>
% endif

${editToolbar('top')}

<div class="row-fluid">
    <div class="span12">
        <h3 class="form-below-toolbar">
        % if isStakeholder:
            ${_('Stakeholder Details')}
        % else:
            ${_('Activity Details')}
        % endif
        </h3>
    </div>
</div>
<div class="row-fluid">
    % if 'id' in cstruct:
        <div class="span12">
            <p class="id">${cstruct['id']}</p>
        </div>
    % endif
</div>

% if not isStakeholder and not empty:
    ## Map container
    <div class="row-fluid">
        <div class="span12 map-not-whole-page">
            <div id="googleMapNotFull">
                <div class="map-form-controls">
                    <div class="form-map-menu pull-right">
                        <button type="button" class="btn btn-mini pull-right form-map-menu-toggle ttip" data-close-text="<i class='icon-remove'></i>" data-toggle="tooltip" title="${_('Turn layers on and off')}"><i class="icon-cog"></i></button>
                        <div class="accordion" id="form-map-menu-content">

                            <!-- This deal -->
                            <div id="thisDealSection" class="map-menu-deals accordion-group">
                                <h6 class="map-deals">
                                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#form-map-menu-content" href="#thisLayer">
                                        <i class="icon-chevron-down"></i>
                                        ${_('This Deal')}
                                    </a>
                                </h6>
                                <div id="thisLayer" class="accordion-body collapse in">
                                    <ul id="map-this-areas-list">
                                        <!-- Placeholder for area entries -->
                                    </ul>
                                </div>
                            </div>

                            <!-- All deals -->
                            <div class="map-menu-deals accordion-group">
                                <h6 class="map-deals">
                                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#form-map-menu-content" href="#contentLayers">
                                        <i class="icon-chevron-right"></i>
                                        ${_('All Deals')}
                                    </a>
                                </h6>
                                <div id="contentLayers" class="accordion-body collapse">
                                    <ul>
                                        <li class="contentLayersMainCheckbox">
                                            <div class="checkbox-modified-small">
                                                <input class="input-top" type="checkbox" id="activityLayerToggle">
                                                <label for="activityLayerToggle"></label>
                                            </div>
                                            <div id="map-deals-symbolization" class="dropdown context-layers-description">
                                                ${_('Loading ...')}
                                            </div>
                                            <ul id="map-points-list" class="hide">
                                                <!-- Placeholder for map points -->
                                            </ul>
                                        </li>
                                    </ul>
                                    <ul id="map-areas-list">
                                        <!-- Placeholder for area entries -->
                                    </ul>
                                </div>
                            </div>

                            <!-- Base layers -->
                            <div class="accordion-group">
                                <h6>
                                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#form-map-menu-content" href="#baseLayers">
                                        <i class="icon-chevron-right"></i>
                                        ${_('Base layers')}
                                    </a>
                                </h6>
                                <div id="baseLayers" class="accordion-body collapse">
                                    <ul>
                                        <li>
                                            <label class="radio inline"><input type="radio" class="baseMapOptions" name="baseMapOptions" id="streetMapOption" value="streetMap" />${_('Street Map')}</label>
                                        </li>
                                        <li>
                                            <label class="radio inline"><input type="radio" class="baseMapOptions" name="baseMapOptions" id="satelliteMapOption" value="satelliteMap" checked="checked" />${_('Satellite Imagery')}</label>
                                        </li>
                                        <li>
                                            <label class="radio inline"><input type="radio" class="baseMapOptions" name="baseMapOptions" id="terrainMapOption" value="terrainMap" />${_('Terrain Map')}</label>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <!-- Context layers -->
                            <div class="accordion-group">
                                <h6>
                                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#form-map-menu-content" href="#contextLayers">
                                        <i class="icon-chevron-right"></i>
                                        ${_('Context layers')}
                                    </a>
                                </h6>
                                <div id="contextLayers" class="accordion-body collapse">
                                    <ul id="context-layers-list">
                                          <!-- Placeholder for context layers entries -->
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
% endif

% for child in field:
    ${child.render_template(field.widget.readonly_item_template)}
% endfor

% if empty:
    <div class="empty-details">
        ${_('This version does not have any attributes to show.')}
    </div>
% endif

${editToolbar('bottom')}

<%def name="editToolbar(position)">
<div class="row-fluid">
  <div class="span12 text-right deal-${position}-toolbar">
    <ul class="inline item-toolbar">
      <li>
        <a href="${request.route_url(historyRouteName, output='html', uid=cstruct['id'])}"><i class="icon-time"></i><span class="link-with-icon">${_('History')}</span></a>
      </li>
      % if request.user and 'id' in cstruct and not empty:
        <li>
          <a href="${request.route_url(routeName, output='form', uid=cstruct['id'], _query=(('v', cstruct['version']),))}"><i class="icon-pencil"></i><span class="link-with-icon">${editLinkText}</span></a>
        </li>
        <li>
          <a href="javascript:void(0);" data-toggle="collapse" data-target="#delete-${form_id}-${position}"><i class="icon-trash"></i><span class="link-with-icon">${deleteLinkText}</span></a>
        </li>
      % endif
      % if request.user and isModerator and statusId == '1':
        <li>
          <a href="${request.route_url(routeName, output='review', uid=cstruct['id'])}"><i class="icon-check"></i><span class="link-with-icon">${_('Review')}</span></a>
        </li>
      % endif
    </ul>
  </div>
</div>
% if request.user and 'id' in cstruct:
  <div id="delete-${form_id}-${position}" class="collapse">
    <form id="${form_id}-${position}" class="delete-confirm alert alert-error" action="${request.route_url(routeName, output='form', uid=cstruct['id'])}" method="POST">
      <input type="hidden" name="__formid__" value="${form_id}"/>
      <input type="hidden" name="id" value="${cstruct['id']}"/>
      <input type="hidden" name="version" value="${cstruct['version']}"/>
      <p>${deleteConfirmText}</p>
      <button name="delete" class="btn btn-small btn-danger">${_('Delete')}</button>
      <button onclick="javascript:console.log($('#delete-${form_id}-${position}')); $('#delete-${form_id}-${position}').collapse('hide'); return false;" class="btn btn-small delete-confirm-cancel">${_('Cancel')}</button>
    </form>
  </div>
% endif
</%def>
