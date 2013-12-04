<%
    isStakeholder = 'itemType' in cstruct and cstruct['itemType'] == 'stakeholders'
    statusId = cstruct['statusId'] if 'statusId' in cstruct else '2'

    from pyramid.security import ACLAllowed
    from pyramid.security import has_permission
    isModerator = isinstance(has_permission('moderate', request.context, request), ACLAllowed)

    from mako.template import Template
    from pyramid.path import AssetResolver
    from lmkp.config import getTemplatePath
    lmkpAssetResolver = AssetResolver('lmkp')
    activitiesResolver = lmkpAssetResolver.resolve(getTemplatePath(request, 'parts/items/activities.mak'))
    activitiesTemplate = Template(filename=activitiesResolver.abspath())
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
                            <!-- Base layers -->
                            <div class="accordion-group">
                                <h6>
                                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#form-map-menu-content" href="#baseLayers">
                                        <b class="caret"></b>${_('Base layers')}
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
                                        <b class="caret"></b>${_('Context layers')}
                                    </a>
                                </h6>
                                <div id="contextLayers" class="accordion-body collapse">
                                    <ul id="context-layers-list">
                                          <!-- Placeholder for context layers entries -->
                                    </ul>
                                </div>
                            </div>
                            <!-- Activity layers -->
                            <div class="accordion-group">
                                <h6>
                                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#form-map-menu-content" href="#activityLayers">
                                        <b class="caret"></b>${activitiesTemplate.render(request=request, _=_)}
                                    </a>
                                </h6>
                                <div id="activityLayers" class="accordion-body collapse">
                                    <ul>
                                        <li>
                                            <div class="checkbox-modified-small">
                                                <input type="checkbox" id="activityLayerToggle" class="input-top">
                                                <label for="activityLayerToggle"></label>
                                            </div>
                                            <p class="context-layers-description">
                                                ${_('Show on map')}
                                            </p>
                                        </li>
                                    </ul>
                                    <div id="map-legend-list">
                                        <!-- Placeholder for legend -->
                                    </div>
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
