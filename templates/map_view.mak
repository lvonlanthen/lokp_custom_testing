<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_('Map View')}</%def>

<%def name="head_tags()">
<link rel="stylesheet" href="${request.static_url('lmkp:static/lib/OpenLayers-2.12/theme/default/style.css')}" type="text/css" />
<script type="text/javascript">
<%
from lmkp.views.profile import _getCurrentProfileExtent
from lmkp.views.views import getOverviewKeys
from lmkp.views.views import getFilterValuesForKey
from lmkp.views.views import getMapSymbolKeys
from lmkp.views.config import form_geomtaggroups
import json

aKeys, shKeys = getOverviewKeys(request)
extent = json.dumps(_getCurrentProfileExtent(request))
mapSymbols = getMapSymbolKeys(request)
mapCriteria = mapSymbols[0]
mapSymbolValues = [v[0] for v in sorted(getFilterValuesForKey(request,
    predefinedType='a', predefinedKey=mapCriteria[1]),
    key=lambda value: value[1])]
geomTaggroups = form_geomtaggroups(request)
%>
    var profilePolygon = ${extent | n};
    var aKeys = ${json.dumps(aKeys) | n};
    var shKeys = ${json.dumps(shKeys) | n};
    var mapValues = ${json.dumps(mapSymbolValues) | n};
    var mapCriteria = ${json.dumps(mapCriteria) | n};
    var areaNames = ${json.dumps(geomTaggroups['mainkeys']) | n};
    var allMapCriteria = ${json.dumps(mapSymbols) | n};

    ## JS Translation
    var tForDeals = '${_("Deal")}';
    var tForInvestor = '${_("Investor")}';
    var tForInvestors = '${_("Investors")}';
    var tForLegend = '${_("Legend")}';
    var tForLegendforcontextlayer = '${_("Legend for context layer")}';
    var tForLoading = '${_("Loading ...")}';
    var tForLoadingdetails = '${_("Loading the details ...")}';
    var tForMoredeals = '${_(" more deals ...")}';
    var tForNodealselected = '${_("No deal selected.")}';
    var tForSelecteddeals = '${_("Selected Deals")}';

</script>
</%def>

## Start of content

## Filter
<%include file="lmkp:customization/testing/templates/parts/filter.mak" />

<!-- content -->
<div id="googleMapFull">
    <!--  Placeholder for the map -->
</div>

<div class="basic-data">
    <h6 class="deal-headline">${_('Deal')}
        <span id="deal-shortid-span" class="underline">#</span>
    </h6>
    <ul id="taggroups-ul">
        <li>
            <p>${_('No deal selected.')}</p>
        </li>
    </ul>
</div>

<!-- map menu -->
<div class="map-menu">
    <form class="navbar-search" action="">
        <input name="q" id="search" class="search-query" placeholder="${_('search location')}" />
        <input value="Search" id="search-submit" />
    </form><br/>
    
    <!-- Deals -->
    <div class="map-menu-deals">
        <h6 class="map-deals">
            <i class="icon-chevron-down"></i>
            ${_('Deals')}
        </h6>
        <div class="map-deals-content">
            <ul>
                <li>
                    <div class="checkbox-modified-small">
                        <input class="input-top" type="checkbox" id="activityLayerToggle" checked="checked">
                        <label for="activityLayerToggle"></label>
                    </div>
                    
                    <div id="map-deals-symbolization" class="dropdown context-layers-description">
                        ${_('Loading ...')}
                    </div>
                    <ul id="map-points-list">
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
    <div class="map-menu-base-layers">
        <h6 class="base-layers">
            <i class="icon-chevron-right"></i>
            ${_('Base layers')}
        </h6>
        <div class="base-layers-content">
            <ul>
                <li>
                    <label class="radio inline"><input type="radio" class="baseMapOptions" name="baseMapOptions" id="streetMapOption" value="streetMap" checked />${_('Street Map')}</label>
                </li>
                <li>
                    <label class="radio inline"><input type="radio" class="baseMapOptions" name="baseMapOptions" id="satelliteMapOption" value="satelliteMap" />${_('Satellite Imagery')}</label>
                </li>
                <li>
                    <label class="radio inline"><input type="radio" class="baseMapOptions" name="baseMapOptions" id="terrainMapOption" value="terrainMap" />${_('Terrain Map')}</label>
                </li>
            </ul>
        </div>
    </div>

    <!-- Context layers -->
    <div class="map-menu-context-layers">
        <h6 class="context-layers">
            <i class="icon-chevron-right"></i>
            ${_('Context layers')}
        </h6>
        <div class="context-layers-content">
            <ul id="context-layers-list">
                <!--  Placeholder for context layers entries -->
            </ul>
        </div>
    </div>
</div>

## End of content

<div id="mapModal" class="modal fade hide">
    <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3 id="mapModalHeader"><!-- Placeholder --></h3>
    </div>
    <div id="mapModalBody" class="modal-body">
        <!-- Placeholder -->
    </div>
    <div class="modal-footer">
        <button id="mapModalClose" class="btn" data-dismiss="modal" aria-hidden="true">${_('Close')}</button>
    </div>
</div>

<%def name="bottom_tags()">
<script type="text/javascript" src="http://maps.google.com/maps/api/js?v=3&amp;sensor=false"></script>
<script src="${request.static_url('lmkp:static/build/openlayers/OpenLayers.mapview.min.js')}" type="text/javascript"></script>
<script type="text/javascript" src="${request.route_url('context_layers')}"></script>
<script src="${request.static_url('lmkp:static/v2/maps/main.js')}" type="text/javascript"></script>
<script src="${request.static_url('lmkp:static/v2/maps/base.js')}" type="text/javascript"></script>
<script src="${request.static_url('lmkp:static/v2/filters.js')}" type="text/javascript"></script>
<script src="${request.static_url('lmkp:static/v2/jquery.cookie.js')}" type="text/javascript"></script>
</%def>