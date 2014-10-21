<%def name="height()">500</%def>

<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_("Charts")}</%def>

<%def name="head_tags()">
  <link rel="stylesheet" href="/custom/css/charts.css"></link>
</%def>

<div class="container">
  <div class="content no-border">
    <div class="row-fluid">
      <div class="pull-right">
        <ul class="nav nav-pills chartNav" id="group-by-pills">
          <!-- Placeholder -->
        </ul>
      </div>
    </div>
    <h4 id="group-by-title"><!-- Placeholder --></h4>
    <div id="loadingRow" class="row-fluid">
      <div class="span12">
        <div id="graphLoading" style="height: ${height()}px;"></div>
      </div>
    </div>
    <div id="chart" class="row-fluid"><!-- Placeholder --></div>
    <div class="row-fluid">
      <div class="btn-group" data-toggle="buttons-radio" id="attribute-buttons"><!-- Placeholder --></div>
      <div class="btn-group btn-bar-sort" data-toggle="buttons-radio">
        <button class="btn" id="sortDesc" data-toggle="tooltip" title="${_('Sort data descending')}">
          <i class="icon-sort-by-attributes-alt"></i>
        </button>
        <button class="btn" id="sortAsc" data-toggle="tooltip" title="${_('Sort data ascending')}">
          <i class="icon-sort-by-attributes"></i>
        </button>
      </div>
    </div>
  </div>
</div>

<%def name="bottom_tags()">
  <script src="${request.static_url('lmkp:static/lib/d3/d3.v3.min.js')}" type="text/javascript"></script>
  <script type="text/javascript">

    var group_activities_by = "${_('Group deals by:')}";
    var show_attribute = "${_('Show attribute:')}";
    var chart_data = {
      item: 'Activity',
      attributes: {
        'Activity': 'count',
        'Intended area (ha)': 'sum'
      },
      groupable: [
        ['Intention of Investment'],
        ['Negotiation Status'],
        ['Implementation status']
      ]
    };
    var attribute_names = [
      "${_('Intended area')}",
      "${_('Deals')}"
    ];

    var current_group_key = "${attr}";
    chart_data['group_by'] = chart_data["groupable"][current_group_key];

    d3.xhr('${request.route_url("evaluation")}')
      .header("Content-Type", "application/json")
      .post(
        JSON.stringify(chart_data),
        function(err, rawData){
          var data = JSON.parse(rawData.responseText);
          if (!data['success']) {
            return console.warn(data['msg']);
          }
          $('#loadingRow').hide();
          visualize(data.data);
        }
      );

    /**
     * Initialize all bootstrap tooltips.
     * https://github.com/twitter/bootstrap/issues/5687#issuecomment-14917403
     */
    $(function () {
      // Tooltips for buttons are placed at the top
      $("button[data-toggle='tooltip']").tooltip({
        container: 'body'
      });
      // Tooltips for links are place at the bottom
      $("a[data-toggle='tooltip']").tooltip({
        container: 'body',
        placement: 'bottom'
      });
    });
  </script>
  <script src="${request.static_url('lmkp:static/v2/charts/barchart.js')}" type="text/javascript"></script>

</%def>
