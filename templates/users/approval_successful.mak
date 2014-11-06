<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_("User Approval Success")}</%def>

<div class="container">
    <div class="content no-border">
        <h3>${_(u"User approval")}</h3>
        <div>
            <p>${_(u"The following user has been successfully approved:")}
            <b>${username}</b></p>
        </div>
    </div>
</div>
