<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_('Deal Editor')}</%def>

<%def name="head_tags()">
    <link rel="stylesheet" href="/static/form.css" type="text/css" />

    <script type="text/javascript" src="${request.static_url('lmkp:static/v2/form.js')}"></script>

    <!-- REQUIREMENTS -->
    <!-- CSS -->
    % for reqt in css_links:
        <link rel="stylesheet" href="/formstatic/${reqt}" type="text/css" />
    % endfor
    % for reqt in js_links:
        <script type="text/javascript" src="/formstatic/${reqt}"></script>
    % endfor

    % if js:
        <script type="text/javascript">${js|n}</script>
    % endif
</%def>

<div class="container deal-edit-content">
    <div class="content no-border">

        ## Session messages
        <%include file="lmkp:templates/parts/sessionmessage.mak"/>

        ${form | n}
    </div>
</div>

<%def name="bottom_tags()">
    <script type="text/javascript">

        var identifier = '${uid}';
        var version = ${version};

        if (deform) {
            deform.load();
        }

        $('button.formdelete').click(function() {
            toggleConfirmDelete();
            return false;
        });
        $('#delete-confirm-cancel').click(function() {
            toggleConfirmDelete();
            return false;
        });

        $(document).ready(function () {
            $('#menu-affix').affix();
            /*
            * Clamped-width.
            * Usage:
            *  <div data-clampedwidth=".myParent">
            *    This long content will force clamped width
            *  </div>
            *
            * Author: LV
            */
            $('[data-clampedwidth]').each(function () {
                var elem = $(this);
                var parentPanel = elem.data('clampedwidth');
                var resizeFn = function () {
                    var sideBarNavWidth = $(parentPanel).width() - parseInt(elem.css('paddingLeft')) - parseInt(elem.css('paddingRight')) - parseInt(elem.css('marginLeft')) - parseInt(elem.css('marginRight')) - parseInt(elem.css('borderLeftWidth')) - parseInt(elem.css('borderRightWidth'));
                    elem.css('width', sideBarNavWidth);
                };

                resizeFn();
                $(window).resize(resizeFn);
            });
        });
    </script>
</%def>
