<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_("[LOKP Stakeholders] Map")}</%def>

<%def name="head_tags()">
  <link rel="stylesheet" href="/custom/css/charts.css"></link>
</%def>

<div class="container">
  <div class="content no-border">
    <div class="row-fluid chart-top-menu">
      <a href="${request.route_url('charts_overview')}">
        <i class="icon-th"></i><span class="link-with-icon">${_("Back to charts overview")}</span>
      </a>
      % if len(profiles) > 0:
        <div class="pull-right">
          <div class="map-profile-select">${_("Profile")}:</div>
          <div class="btn-group">
            <button class="btn btn-country-selector">${profile}</button>
            <button class="btn btn_favorite_right dropdown-toggle" data-toggle="dropdown">
              <i class="icon-caret-down"></i>
            </button>
            <ul class="dropdown-menu" id="profile-selector">
              % for p in profiles:
                <li><a href="javascript:void(0);" data-profile="${p[1]}">${p[0]}</a></li>
              % endfor
            </ul>
          </div>
        </div>
      % endif
    </div>
    <div class="row-fluid visible-phone">
      <h2 class="chart-title"><!-- Placeholder --></h2>
    </div>
    <div id="map" class="row-fluid">
      <div id="loading-div">
        <div id="graphLoading" style="height: 200px;"></div>
      </div>
    </div>
    <div class="row-fluid">
      <div class="span6 hidden-phone">
        <div id="country-details"></div>
        <div id="helptext" class="hide">
          <h2 class="chart-title"></h2>
          <p>${_('The map shows the country of origin of [LOKP Stakeholders] involved in [LOKP Activities] from the selected profile.')}</p>
          <p>${_('The colors represent the number of [LOKP Stakeholders] from a certain country. The darker the color, the more [LOKP Stakeholders].')}</p>
          <p>${_('Move your mouse over a country in the list or on the map to show the details.')}</p>
        </div>
      </div>
      <div class="span6">
        <ul id="countries-list"><!-- Placeholder --></ul>
      </div>
    </div>
  </div>
</div>

<%def name="bottom_tags()">
  <script src="${request.static_url('lmkp:static/lib/d3/d3.v3.min.js')}"></script>
  <script src="${request.static_url('lmkp:static/lib/d3/colorbrewer.v1.min.js')}"></script>
  <script src="${request.static_url('lmkp:static/lib/d3/topojson.v1.min.js')}"></script>
  <script src="${request.static_url('lmkp:static/v2/charts/mapchart.js')}" type="text/javascript"></script>
  <script type="text/javascript">

    var attributeNames = [
      "${_('[LOKP Stakeholder]')}"
    ];
    var chartData = {
      'item': 'Stakeholder',
      'attributes': {
        'Stakeholder': 'count'
      },
      'group_by': ['Country of origin'],
      'locales': ['code'],
      'translate': {
        'keys': [['Country of origin']]
      }
    };
    var data_url = '${request.route_url("evaluation")}';
    var map_url = '${request.static_url("lmkp:static/v2/charts/world.topo.json")}';

    drawMap();
    loadMapData();

    $('#profile-selector>li>a').click(function() {
      $('.btn-country-selector').text($(this).text());
      changeProfile($(this).data('profile'));
    });
  </script>
</%def>
