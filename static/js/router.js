/*
 * 
 * ATW.router.js
 * 
 */


(function(undefined){
    var Router =  Backbone.Router.extend({
        navigate:function(route, options){
            options = _.extend({trigger: true}, options);
            if((typeof OWATracker) !== 'undefined')
            {
                OWATracker.trackAction('Navigation', route);
            }
            Backbone.Router.prototype.navigate.apply(this, [route, options]);
        },
        routes:{
            '': 'home',
            'visit': 'visit',
            'episode/:id': 'episode',
            'register': 'register',
            'profile' : 'profile',
            'logout': 'logout',
            'setlang/:code':'setlang',
        },
        home:function(){
            if(!app.isLogged())
            {
                app.setComponents('home audio register visit login agenda'.split(' '));
                app.playAudio('/static/home.mp3');
            }
            else
                this.visit();
        },
        visit:function(){
            app.setComponents('player login agenda'.split(' '));
            app.playDefault();
        },
        episode:function(id){
            app.setComponents('player login agenda'.split(' '));
            app.playEpisode(id);
        },
        register:function(){
            app.setComponents('home audio register'.split(' '));
            app.playAudio('/static/home.m4a');
        },
        profile:function(){
            if(!app.isLogged())
            {
                this.navigate('register');
            }
            else
            {
                app.setComponents('profile'.split(' '));
            }
        },
        logout:function(){
            $.ajax({
                type: "GET",
                url: '/logout',
                data: {  },
                dataType: 'json'
            });
            ATW.Config.user_name = undefined;
            ATW.Config.api_key = undefined;
            app.resetViews(['login','contact']);
            this.navigate('visit');
        },
        setlang:function(code){
            var self = this;
            $.ajax({
                type: "POST",
                url: '/i18n/setlang/',
                data: { language:code },
//                    dataType: 'json'
            });
            var href = window.location.href;
            var baseloc= href.protocol + '//'+ href.host
            href = baseloc;
        },
    });
    
    ATW.Router = Router;
})();


