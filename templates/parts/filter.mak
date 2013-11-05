<%doc>
    This is the template for the filter area.
</%doc>

<%
    from lmkp.views.views import getFilterKeys
    from lmkp.views.views import getActiveFilters

    aFilterKeys, shFilterKeys = getFilterKeys(request)
    activeFilters = getActiveFilters(request)
%>

## JS Translations
<script type="text/javascript">
    var tForValue = "${_('Value')}";
</script>

<div class="form-horizontal filter_area">
    <div class="container">
        ## Show all active filters
        % for i, a in enumerate(activeFilters):
            <div class="control-group active-filter">
                % if i == 0:
                    <label class="control-label">${_('Active Filters')}</label>
                % endif
                <div class="controls">
                    <input type="text" class="filter-variable${i+1}" value="${a[1]}"/>
                    <input id="active-filter-${i+1}" type="hidden" value="${a[0]}"/>
                    <span class="icon-remove${i+1}" onclick="javascript:deleteFilter(${i+1});">
                        <i class="icon-remove pointer"></i>
                    </span>
                </div>
            </div>
        % endfor

        ## Show form to add a new filter
        <div class="control-group new-filter new-filter">
            <label class="control-label">${_('New Filter')}</label>
            <div class="controls">
                ## Key
                <div class="btn-group input-append">
                    <input id="new-filter-key" class="select_btn_filter" type="text" placeholder="${_('Key')}" />
                    <input id="new-filter-key-internal" type="hidden" value=""/>
                    <input id="new-filter-itemtype" type="hidden" value="a"/>
                    <button class="btn select_btn_filter_right dropdown-toggle" data-toggle="dropdown">
                        <span class="caret"></span>
                    </button>
                    <ul class="dropdown-menu pull-right" role="menu">
                        <li class="disabled filterCategory">${_('Deals')}</li>
                        % for k in aFilterKeys:
                            <li><a href="#" onClick="javascript:selectKey('${k[0]}', '${k[1]}', '${k[2]}', 'a')">${k[0]}</a></li>
                        % endfor
                        <li class="disabled filterCategory">${_('Investors')}</li>
                        % for k in shFilterKeys:
                            <li><a href="#" onClick="javascript:selectKey('${k[0]}', '${k[1]}', '${k[2]}', 'sh')">${k[0]}</a></li>
                        % endfor
                    </ul>
                </div>
                ## Operator
                <div class="btn-group">
                    <button id="new-filter-operator-display" class="btn select_btn_operator"></button>
                    <input id="new-filter-operator" type="hidden" />
                    <button class="btn select_btn_operator_right dropdown-toggle" data-toggle="dropdown">
                        <span class="caret"></span>
                    </button>
                    <ul id="new-filter-operator-dropdown" class="dropdown-menu small">
                        <!-- Placeholder for the operators -->
                    </ul>
                </div>
                ## Value
                <div id="new-filter-value-box" class="btn-group">
                    <!-- will be replaced -->
                    <input id="new-filter-value-internal" type="text" class="filter-value" placeholder="${_('Value')}" />
                </div>
                <span class="icon-add" onClick="javascript:addNewFilter();">
                    <i class="icon-plus pointer"></i>
                </span>
            </div>
        </div>
<!--        <div class="favorite">
            <div class="btn-group favorite">
                <button class="btn btn_favorite">Favorite</button>
                <button class="btn btn_favorite_right dropdown-toggle" data-toggle="dropdown">
                    <span class="caret"></span>
                </button>
                <ul class="dropdown-menu">
                    <li><a href="#">1</a></li>
                    <li><a href="#">2</a></li>
                    <li><a href="#">3</a></li>
                    <li><a href="#">4</a></li>
                    <li><a href="#">5</a></li>
                </ul>
            </div>
        </div>-->
    </div>
</div>

<div class="filter_area_openclose">
    <i class="icon-double-angle-down pointer"></i>
    % if len(activeFilters) == 1:
        <span class="pointer">${len(activeFilters)} ${_('filter is active, click here to edit')}</span>
    % elif len(activeFilters) > 1:
        <span class="pointer">${len(activeFilters)} ${_('filters are active, click here to edit')}</span>
    % else:
        <span class="pointer">${_('Click here to add a filter')}</span>
    % endif
    <i class="icon-double-angle-down pointer"></i>
</div>