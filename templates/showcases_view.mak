<%inherit file="lmkp:customization/testing/templates/base_no_menu.mak" />
<%page expression_filter="h"/>

<%def name="title()">${_('Show cases')}</%def>

<%def name="head_tags()">
</%def>

<%def name="body()">
    <div class="row-fluid blog-content">
        <div class="span10 offset1">
            <p>Showcases</p>
        </div>
    </div>
</%def>

<%def name="bottom_tags()">
    <script src="/custom/js/vendor/bootstrap-lightbox.min.js"></script>
</%def>
