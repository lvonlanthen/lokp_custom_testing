<%
from lmkp.utils import handle_query_string
from lmkp.views.translation import get_languages
from lmkp.views.translation import get_profiles
languages = get_languages()
selectedlanguage = languages[0]
for l in languages:
    if locale == l[0]:
        selectedlanguage = l
profiles = get_profiles()
selectedprofile = None
for p in profiles:
   if profile == p[0]:
       selectedprofile = p
mode = None
if 'lmkp.mode' in request.registry.settings:
    if str(request.registry.settings['lmkp.mode']).lower() == 'demo':
        mode = 'demo'

use_piwik_analytics = False
if 'lmkp.use_piwik_analytics' in request.registry.settings:
    if str(request.registry.settings['lmkp.use_piwik_analytics']).lower() == "true":
        use_piwik_analytics = True
%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!--[if lt IE 7]>      <html xmlns="http://www.w3.org/1999/xhtml" class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html xmlns="http://www.w3.org/1999/xhtml" class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html xmlns="http://www.w3.org/1999/xhtml" class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html xmlns="http://www.w3.org/1999/xhtml" class="no-js"> <!--<![endif]-->
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="content-language" content="${selectedlanguage[0]}" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
        <link rel="icon" type="image/ico" href="/custom/img/favicon.ico"/>
        <title>
            <%
                try:
                    context.write("%s - %s" % (self.title(), _("LOKP")))
                except AttributeError:
                    context.write(_("LOKP"))
            %>
        </title>
        <meta name="description" content="" />
        <meta name="viewport" content="width=device-width" />

        <link rel="stylesheet" href="/custom/css/bootstrap-combined.no-icons.min.css"></link>
        <link rel="stylesheet" href="/custom/css/font-awesome/css/font-awesome.min.css"></link>

        <link rel="stylesheet" href="/custom/css/bootstrap-responsive.min.css"></link>
        <link rel="stylesheet" href="/custom/css/main.css"></link>

        <link rel="stylesheet" href="/custom/css/custom.css"></link>

        <!--[if IE 7]>

            <link rel="stylesheet" href="/custom/css/ie7.css"></link>
            <link rel="stylesheet" href="/custom/css/font-awesome/css/font-awesome-ie7.css"></link>

        <![endif]-->


        <!--[if IE 8]>

            <link rel="stylesheet" href="/custom/css/ie8.css"></link>

        <![endif]-->

        <script type="text/javascript" src="/custom/js/vendor/modernizr-2.6.2-respond-1.1.0.min.js"></script>

        ## Include the head tags of the child template if available.
        <%
            try:
                self.head_tags()
            except AttributeError:
                pass
        %>

    </head>
    <body>
        <!--[if lt IE 7]>
            <p class="chromeframe">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> or <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a> to improve your experience.</p>
        <![endif]-->

        <div class="wrap">
            <div id="main" class="clearfix">

                ## Header

                <div class="navbar header_self">
                    <div class="container">
                        <div class="logo">
                            <a href="${request.route_url('profile_global')}">
                                % if mode == 'demo':
                                    <img src="/custom/img/logo_demo.png" alt="${_('LOKP')}" />
                                % else:
                                    <img src="/custom/img/logo.png" alt="${_('LOKP')}" />
                                % endif
                            </a>
                        </div>
                        <ul class="top-menu">
                            <%
                                # The entries of the top menus as arrays
                                # with
                                # - an array of urls (the first one being used for the link)
                                # - icon (li class)
                                # - name
                                topmenu = [
                                    [
                                        [request.route_url('map_view')],
                                        'icon-map-marker',
                                        _('Map')
                                    ], [
                                        [
                                            request.route_url('grid_view'),
                                            request.route_url('activities_read_many', output='html'),
                                            request.route_url('stakeholders_read_many', output='html'),
                                            request.route_url('stakeholders_byactivities_all', output='html')
                                        ],
                                        'icon-align-justify',
                                        _('Grid')
                                    ], [
                                        [
                                            request.route_url('charts_view'),
                                            request.route_url('charts_overview')
                                        ],
                                        'icon-bar-chart',
                                        _('Charts')
                                    ]
                                ]
                            %>

                            % for t in topmenu:
                                <li
                                    % if request.current_route_url() in t[0]:
                                        class="active grid"
                                    % endif
                                    >
                                    <a href="${t[0][0]}${handle_query_string(request.url, return_value='query_string', remove=['bbox', 'order_by', 'dir', 'status'])}">
                                        <i class="${t[1]}"></i><span class="hidden-verysmall">&nbsp;&nbsp;${t[2]}</span>
                                    </a>
                                </li>
                            % endfor

                            ## If the user is logged in, show link to add a new deal
                            % if request.user:
                                <li
                                    % if request.current_route_url() == request.route_url('activities_read_many', output='form'):
                                        class="active grid"
                                    % endif
                                    >
                                    <a href="${request.route_url('activities_read_many', output='form')}" >
                                        <i class="icon-pencil"></i>
                                        <span class="hidden-verysmall">${_('New Deal')}</span>
                                    </a>
                                </li>
                            % endif
                        </ul>
                        <div class="user">
                            <ul class="nav nav-pills">
                                % if request.user is None:
                                    <li class="active">
                                        <div>
                                            <a class="blacktemp" href="${request.route_url('login_form')}">
                                                ${_('Login')}
                                            </a>
                                        </div>
                                    </li>
                                    % if mode != 'demo':
                                        <li>/</li>
                                        <li class="active">
                                            <div>
                                                <a class="blacktemp" href="${request.route_url('user_self_registration')}">
                                                    ${_('Register')}
                                                </a>
                                            </div>
                                        </li>
                                    % endif
                                % else:
                                    <li>
                                        <div>
                                            <a class="blacklink" href="${request.route_url('user_account')}">${request.user.username}</a>
                                            (<a href="${request.route_url('logout')}" class="blacklink">${_('Logout')}</a>)&nbsp;&nbsp;
                                        </div>
                                    </li>
                                % endif

                                <li>|</li>
                                <li>
                                    <div class="dropdown">
                                        <a class="dropdown-toggle blacktemp" data-toggle="dropdown" href="#">
                                            <span class="link-icon-right">${selectedlanguage[1]}</span><b class="caret"></b>
                                        </a>
                                        <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                            % for l in languages:
                                                <li class="cursor">
                                                    <a href="${handle_query_string(request.url, add=[('_LOCALE_', l[0])])}">${l[1]}</a>
                                                </li>
                                            % endfor
                                        </ul>
                                    </div>
                                </li>
                                % if len(profiles) >= 1:
                                   <li>|</li>
                                   <li>
                                       <div class="dropdown">
                                           <a class="dropdown-toggle blacktemp" data-toggle="dropdown" href="#">
                                               % if selectedprofile is None:
                                                   ${_('Select Profile')}
                                               % else:
                                                   ${selectedprofile[1]}
                                               % endif
                                               <b class="caret"></b>
                                           </a>
                                           <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu">
                                               % for p in profiles:
                                                   <li class="cursor">
                                                       <a href="/${p[0]}">${p[1]}</a>
                                                   </li>
                                               % endfor
                                           </ul>
                                       </div>
                                   </li>
                               % endif
                            </ul>
                        </div>
                    </div>
                </div>

                ## End of Header

                ## Content

                ## Use the body of the child template
                ${self.body()}

                ## End of Content

            </div>
            <div class="push"></div>
        </div>

        ## Footer

        <div class="navbar footer">
            <ul class="nav pull-right">

                <%
                # The entries of the footer as arrays with
                # - url
                # - name
                footer = [
                    [request.route_url('faq_view'), _('FAQ')],
                    [request.route_url('about_view'), _('About')],
                    [request.route_url('partners_view'), _('Partners & Donors')]
                ]
                %>

                % for f in footer:
                    <li
                        % if request.current_route_url() == f[0]:
                            class="active"
                        % endif
                        >
                        <a href="${f[0]}">${f[1]}</a>
                    </li>
                % endfor
            </ul>
        </div>

        ## End of Footer

        <script type="text/javascript">
         /* <![CDATA[ */
         document.write(unescape("%3Cscript src='" + (("https:" == document.location.protocol) ? "https://" : "http://") + "www.google.com/jsapi' type='text/javascript'%3E%3C/script%3E"));
         /* ]]> */
        </script>

<!--        <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>-->
        <script>window.jQuery || document.write('<script type="text/javascript" src="/custom/js/vendor/jquery-1.9.1.min.js"><\/script>')</script>

        <script type="text/javascript" src="/custom/js/vendor/bootstrap.min.js"></script>

        <script type="text/javascript" src="${request.static_url('lmkp:static/v2/main.js')}"></script>

        % if use_piwik_analytics==True:
        <!-- Piwik -->
        <script type="text/javascript">
          var _paq = _paq || [];
          % if selectedprofile is not None:
          _paq.push(["setCustomVariable", 1, "profile", "${selectedprofile[0]}", "page"])
          % else:
          _paq.push(["setCustomVariable", 1, "profile", "none", "page"])
          % endif
          _paq.push(["trackPageView"]);
          _paq.push(["enableLinkTracking"]);

          (function() {
            var u=(("https:" == document.location.protocol) ? "https" : "http") + "://webstats.landobservatory.org/";
            _paq.push(["setTrackerUrl", u+"piwik.php"]);
            _paq.push(["setSiteId", "1"]);
            var d=document, g=d.createElement("script"), s=d.getElementsByTagName("script")[0]; g.type="text/javascript";
            g.defer=true; g.async=true; g.src=u+"piwik.js"; s.parentNode.insertBefore(g,s);
          })();
        </script>
        <!-- End Piwik Code -->
        % endif

        ## Include the bottom tags of the child template if available.
        <%
            try:
                self.bottom_tags()
            except AttributeError:
                pass
        %>

    </body>

</html>
