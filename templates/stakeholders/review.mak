<%inherit file="lmkp:customization/testing/templates/stakeholders/compare.mak" />

<%def name="title()">${_('Investor Moderation')}</%def>

<%def name="topOfForm()">
    <h3>${_('Investor Moderation')}</h3>
    <p class="id">${identifier}</p>
    <div class="row-fluid">
        <div class="span6">
            <div class="row-fluid">
                <ul class="nav nav-tabs table_tabs">
                    <li class="active">
                        <a href="" onclick="javascript:return false;">
                            % if refMetadata:
                                ${refMetadata['status']}
                            % else:
                                -
                            % endif
                        </a>
                    </li>
                </ul>
            </div>
            % if refMetadata:
            <div class="row-fluid">
                <div class="span12 grid-area border-bottom deal-data">
                    <div class="span5">
                        <h5 class="green">
                            ${_('Version')}
                        </h5>
                    </div>
                    <div class="span7">
                        ${refVersion}
                    </div>
                    <div class="row-fluid">
                        <div class="span5">
                            <h5 class="green moderate-metadata">
                                ${_('Timestamp')}
                            </h5>
                        </div>
                        <div class="span7">
                            ${refMetadata['timestamp']}
                        </div>
                    </div>
                    <div class="row-fluid">
                        <div class="span5">
                            <h5 class="green moderate-metadata">
                                ${_('User')}
                            </h5>
                        </div>
                        <div class="span7">
                            ${refMetadata['username']}
                        </div>
                    </div>
                </div>
            </div>
            % else:
            <div class="row-fluid">
                <div class="span12 grid-area deal-data">
                    ${_('There is no previous version available.')}
                </div>
            </div>
            % endif
        </div>
        <div class="span6">
            <div class="row-fluid">
                <div class="span3">
                    <ul class="nav nav-tabs table_tabs">
                        <li class="active">
                            <a href="" onclick="javascript:return false;">
                                ${newMetadata['status']}
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="span6">
                    % if len(pendingVersions) > 1:
                    <div class="btn-group">
                        <button class="btn select_btn_bordered"></button>
                        <button class="btn select_btn_bordered_right dropdown-toggle" data-toggle="dropdown">
                            <span class="caret"></span>
                        </button>
                        <ul class="dropdown-menu">
                            % for pV in pendingVersions:
                            <li>
                                <a href="?new=${pV}">${_('Version')} ${pV}</a>
                            </li>
                            % endfor
                        </ul>
                    </div>
                    % endif
                </div>
                <div class="span3">
                    <ul class="nav nav-tabs table_tabs">
                        <li>
                            <a href="${request.route_url('stakeholders_read_one_history', output='html', uid=identifier)}">${_('History')}</a>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="row-fluid">
                <div class="span12 grid-area border-bottom deal-data">
                    <div class="span5">
                        <h5 class="green">
                            ${_('Version')}
                        </h5>
                    </div>
                    <div class="span7">
                        ${newVersion}
                    </div>
                    <div class="row-fluid">
                        <div class="span5">
                            <h5 class="green moderate-metadata">
                                ${_('Timestamp')}
                            </h5>
                        </div>
                        <div class="span7">
                            ${newMetadata['timestamp']}
                        </div>
                    </div>
                    <div class="row-fluid">
                        <div class="span5">
                            <h5 class="green moderate-metadata">
                                ${_('User')}
                            </h5>
                        </div>
                        <div class="span7">
                            ${newMetadata['username']}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</%def>

<%def name="moderate_buttons()">
    <form class="moderate-form" action="${request.route_url('stakeholders_review')}" method="POST">
        <div class="row-fluid">
                <div class="span4">
                    % if reviewable is True:
                        <button name="review_decision" value="approve" class="btn btn-large btn-block disabled btn-success deal-moderate-button">
                            ${_('Approve')}
                        </button>
                    % else:
                        <button name="review_decision" value="approve" class="btn btn-large btn-block disabled" onclick="javascript:return false;">
                            [ ${_('Approve')} ]
                        </button>
                    % endif
                </div>
                <div class="span4">
                    <button name="review_decision" value="reject" class="btn btn-large btn-block disabled btn-warning deal-moderate-button">
                        ${_('Deny')}
                    </button>
                </div>
                <div class="span4">
                    <a class="btn btn-large btn-block disabled btn-warning deal-moderate-button" href="${request.route_url('stakeholders_read_one', output='form', uid=identifier, _query=(('v', newVersion),))}">
                        ${_('Edit')} (${_('Version')} ${newVersion})
                    </a>
                </div>
                <input type="hidden" name="identifier" value="${identifier}">
                <input type="hidden" name="version" value="${newVersion}">
                <input type="hidden" name="camefrom" value="${camefrom}">
        </div>
        % if len(missingKeys) > 0:
            <div class="alert alert-danger alert-block alert-missing-mandatory-keys">
                <p><strong>${_('Warning')}</strong></p>
                <p>${_('There are some mandatory keys missing. The item cannot be approved without these keys. Please click the "edit" button to add the missing keys.')}</p>
                <p>${_('The following keys are missing:')}</p>
                <ul class="bullets">
                % for m in missingKeys:
                    <li>${m}</li>
                % endfor
                </ul>
            </div>
        % endif
        % if reviewableMessage:
            <div class="alert alert-danger alert-block alert-missing-mandatory-keys">
                <p><strong>${_('Warning')}</strong></p>
                <p>${reviewableMessage}</p>
            </div>
        % endif
        % if recalculated:
            <div class="alert alert-info alert-block alert-recalculated-version">
                <p><strong>${_('Notice')}</strong></p>
                <p>${_('The two versions are not based directly on each other. The new version is calculated to display only the changes made to this version. Approving it will create a new version.')}</p>
            </div>
        % endif
        <div class="row-fluid comments">
            <div class="span12">
                <div class="span5">
                    <h5 class="green">
                        ${_('Additional comments')}
                    </h5>
                </div>
                <div class="span7">
                    <textarea name="review_comment" class="input-style" rows="4"></textarea>
                </div>
            </div>
        </div>
    </form>
</%def>

${parent.body()}
