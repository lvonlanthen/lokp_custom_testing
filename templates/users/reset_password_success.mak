<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_('Password Reset Successful')}</%def>

<div class="container">
    <div class="content no-border">
        <div class="row-fluid">
            <div class="span8 offset2">
                <h3>${_('Password Reset Successful')}</h3>
            </div>
        </div>
        <div class="row-fluid">
            <div class="span8 offset2">
                <div class="alert alert-success">
                    ${_(u"Password reset was successful. An email containing the new password has been sent to your email address.")}
                </div>
            </div>
        </div>
        <div class="row-fluid">
            <div class="span8 offset2">
                <a href="${request.route_url('login_form')}">${_(u"Proceed to the login page")}</a>
            </div>
        </div>
    </div>
</div>