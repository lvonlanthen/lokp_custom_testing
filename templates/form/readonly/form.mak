<%
    isStakeholder = 'itemType' in cstruct and cstruct['itemType'] == 'stakeholders'
    statusId = cstruct['statusId'] if 'statusId' in cstruct else '2'

    from pyramid.security import ACLAllowed
    from pyramid.security import has_permission
    isModerator = isinstance(has_permission('moderate', request.context, request), ACLAllowed)

    if isStakeholder:
        routeName = 'stakeholders_read_one'
        editLinkText = _('Edit this Investor')
    else:
        routeName = 'activities_read_one'
        editLinkText = _('Edit this Deal')
%>

% if statusId != '2':
    <div class="row-fluid">
        <div class="span9">
            <div class="alert alert-block">
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
    </div>
% endif

<div class="row-fluid">
    <div class="span9 text-right">
        ${editToolbar(True)}
    </div>
</div>

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
        <div class="span9">
            <p class="id">${cstruct['id']}</p>
        </div>
    % endif
</div>

% if not isStakeholder:
    ## Map container
    <div class="row-fluid">
        <div class="span9 map-not-whole-page">
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

<div class="span12">
    ${editToolbar(False)}
</div>

<%def name="editToolbar(top)">
% if top is False:
    <p>&nbsp;</p>
% endif
<div class="row-fluid">
    <a href="${request.route_url(routeName, output='history', uid=cstruct['id'])}">
        <i class="icon-time"></i>&nbsp;${_('History')}
    </a>
    % if request.user and 'id' in cstruct:
        &nbsp;|&nbsp;<a href="${request.route_url(routeName, output='form', uid=cstruct['id'], _query=(('v', cstruct['version']),))}">
            <i class="icon-pencil"></i>&nbsp;${editLinkText}
        </a>
        % if isModerator and statusId == '1':
            &nbsp;|&nbsp;<a href="${request.route_url(routeName, output='review', uid=cstruct['id'])}">
                <i class="icon-check"></i>&nbsp;${_('Review')}
            </a>
        % endif
    % endif
</div>
</%def>