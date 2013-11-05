${field.start_mapping()}

% for child in field.children:
    ${child.render_template(field.widget.item_template)}
% endfor

${field.end_mapping()}

<%
    import colander
    import json
    newForm = 'id' in cstruct and cstruct['id'] == colander.null
    _ = request.translate
%>

<p>
    <a
        id="remove-involvement-${field.oid}"
        href=""
        class="btn btn-small btn-warning remove-involvement"
        onclick="return removeInvolvement(this);"
        % if newForm:
            style="display:none;"
        % endif
        >
        <i class="icon-remove"></i>
        ${_('Remove the Stakeholder')}
    </a>
</p>

<div class="accordion add-involvement" id="accordion-${field.oid}">
    <div class="accordion-group">
        <div class="accordion-heading">
            <a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion-${field.oid}" href="#accordion-content-${field.oid}">
                <i class="icon-plus"></i> ${_('Select a Stakeholder')}
            </a>
        </div>
        <div id="accordion-content-${field.oid}" class="accordion-body collapse">
            <div class="accordion-inner">
                <p>
                    ${_('Search the database to find an existing Stakeholder. Start typing (at least 4 characters) to search a Stakeholder and select it.')}
                </p>

                <div class="input-prepend">
                  <span class="add-on"><i class="icon-search"></i></span>
                  <input class="span12" id="searchinvinput-${field.oid}" type="text" placeholder="${_('Search a Stakeholder')}">
                </div>

                <hr class="grey"/>

                <p>
                    ${_('Nothing found? Maybe the Stakeholder is not yet in the database. You can create a new Stakeholder.')}
                </p>
                    <button id="create_involvement"
                            class="btn btn-small btn-primary"
                            value="createinvolvement"
                            name="createinvolvement_${field.name}">
                        <i class="icon-pencil"></i>&nbsp;&nbsp;${_('Create a new Stakeholder')}
                    </button>
            </div>
        </div>
    </div>
</div>

<%
    import json
    from lmkp.views.views import getOverviewKeys
    aKeys, shKeys = getOverviewKeys(request)
%>

<script type="text/javascript">
    var tForUnknown = "${_('Unknown')}";
    var tForNothingfound = "${_('No results found.')}";
    var tForToomanyresults = "${_('Too many results to display. Try to enter more characters')}";

    var searchPrefix = 'sh';
    var queryUrl = "${request.route_url('stakeholders_read_many', output='json')}";
    var shKeys = ${json.dumps(shKeys) | n};

    deform.addCallback(
        'searchinvinput-${field.oid}',
        function(oid) {
            createSearch(oid, tForUnknown, tForToomanyresults, tForNothingfound,
                queryUrl, searchPrefix, shKeys);
        }
    );
</script>
