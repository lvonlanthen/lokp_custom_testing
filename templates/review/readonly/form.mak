<%
    isStakeholder = 'itemType' in cstruct and cstruct['itemType'] == 'stakeholders'
    statusId = cstruct['statusId'] if 'statusId' in cstruct else '2'

    from pyramid.security import ACLAllowed
    from pyramid.security import has_permission
    isModerator = isinstance(has_permission('moderate', request.context, request), ACLAllowed)
%>

% if not isStakeholder:
## Map container
<div class="row-fluid accordion accordion-group">
    <div class="accordion-heading category" id="form-map-compare-heading">
        <div class="span12">
            <a class="accordion-toggle" data-toggle="collapse" href="#collapse-map">
                ${_('Map')}
                <i class="icon-chevron-down"></i>
            </a>
        </div>
    </div>
    <div id="collapse-map" class="row-fluid accordion-body collapse">
        <div class="span12">
            <div id="googleMapNotFull">
                <div class="form-map-compare-controls">
                    <div class="form-map-compare-legend row-fluid">
                        <div id="refMapLegend" class="span6 hide">
                            <div class="checkbox-modified-small">
                                <input type="checkbox" id="refLayerToggle" class="input-top" checked="checked">
                                <label for="refLayerToggle"></label>
                            </div>
                            <p class="context-layers-description">
                                <span class="compare-legend" style="background:#00ccff;">&nbsp;</span>
                                <span id="refMapLegendEntry"></span>
                            </p>
                        </div>
                        <div id="newMapLegend" class="span6 hide">
                            <div class="checkbox-modified-small">
                                <input type="checkbox" id="newLayerToggle" class="input-top" checked="checked">
                                <label for="newLayerToggle"></label>
                            </div>
                            <p class="context-layers-description">
                                <span class="compare-legend" style="background:#ffcc00;">&nbsp;</span>
                                <span id="newMapLegendEntry"></span>
                            </p>
                        </div>
                    </div>
                    <div class="form-map-compare-menu">
                        <button type="button" class="btn btn-mini pull-right form-map-menu-toggle ttip" data-close-text="<i class='icon-remove'></i>" data-toggle="tooltip" title="${_('Turn layers on and off')}"><i class="icon-cog"></i></button>
                        <div class="accordion" id="form-map-menu-content">
                            
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
</div>
% endif

% for child in field:
    ${child.render_template(field.widget.readonly_item_template)}
% endfor
