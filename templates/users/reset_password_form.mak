<%inherit file="lmkp:customization/testing/templates/base.mak" />

<%def name="title()">${_('Password Reset')}</%def>

<div class="container">
    <div class="content no-border">
        <div class="row-fluid">
            <div class="span4 offset4">
                <h3>${_('Password Reset')}</h3>


            </div>
        </div>
        % if warning is not None:
        <div class="row-fluid">
            <div class="span4 offset4">
                <div class="alert alert-error">
                    ${warning | n}
                </div>
            </div>
        </div>
        % endif
        <div class="row-fluid">
            <div class="span4 offset4">
                <form action="/reset" method="POST">
                    <fieldset class="simple_login">
                        <label for="login">${_(u"Username")}:</label>
                        <input class="input-style span12" type="text" id="username-input" name="username" /><br />
                        <input type="hidden" name="came_from" value="${came_from}"/><br />
                        <input class="btn btn-primary" type="submit" name="form.submitted" value="${_('Reset')}"/>
                    </fieldset>
                </form>
            </div>

        </div>
    </div>
</div>