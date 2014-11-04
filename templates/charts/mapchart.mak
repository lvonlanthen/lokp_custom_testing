<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_("[LOKP Stakeholders] Map")}</%def>

<%def name="head_tags()">
  <link rel="stylesheet" href="/custom/css/charts.css"></link>
</%def>

<div class="container">
  <div class="content no-border">
    <div class="row-fluid visible-phone">
      <h2 class="chart-title"></h2>
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
          <p>${_('The colors represent the number of [LOKP Stakeholders] from this country. The darker the color, the more [LOKP Stakeholders].')}</p>
          <p>${_('Move your mouse over a country in the list or on the map to show the details.')}</p>
        </div>
      </div>
      <div class="span6">
        <ul id="countries-list">
        </ul>
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

    d3.xhr('${request.route_url("evaluation")}')
      .header('Content-Type', 'application/json')
      .post(
        JSON.stringify(chartData), function (error, rawData) {
          var data = JSON.parse(rawData.responseText);
          if (!data['success']) {
            return console.warn(data['msg']);
          }
          updateContent(data);
          visualize(data.data);
        }
      );
  </script>
</%def>
